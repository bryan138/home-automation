#!/usr/bin/python


import os
import sys
import socket
import datetime
import subprocess

from time import sleep
from datetime import datetime, time


import fauxmo
import logging
import time

from debounce_handler import debounce_handler


USERNAME = "username"
PASSWORD = "password"
SERVER_IP = "192.168.1.101"


def log(title, message):
    now = datetime.now()
    date = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    hour = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

    # Pushbullet
    cmd(["/usr/local/Scripts/pushbullet.sh", title, hour + ": " + message])

    # Log file
    file = open("/usr/local/Scripts/Logs/" + ((sys.argv[0]).split("/")[-1])[:-3] + ".txt", "a")
    file.write(date + " " + hour + ": " + title + ". " + message + "\n")
    file.close()

def cmd(args):
    output = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = str(output.stdout.read())
    return out.split("\n")



class PC(debounce_handler):
    def __init__(self):
        super(PC, self).__init__()
        self.name = "PC"
        self.port = 52000

    def act(self, client_address, state):
        print "PC: State", state, "from client @", client_address

        if (state):
            # Wake on lan
            cmd(["sudo", "python", "/home/osmc/code/wake_on_lan.py"])
        else:
            # Turn off PC
            cmd(["net", "rpc", "shutdown", "-t", "30", "-I", SERVER_IP, "-U", USERNAME + "%" + PASSWORD])

        return True

class Speaker(debounce_handler):
    def __init__(self):
        super(Speaker, self).__init__()
        self.name = "Speakers"
        self.port = 52001

    def act(self, client_address, state):
        print "Speaker: State", state, "from client @", client_address

        if (state):
            cmd(["sudo", "python", "/home/osmc/code/home-automation/gpio_write.py", "8", "0"])
        else:
            cmd(["sudo", "python", "/home/osmc/code/home-automation/gpio_write.py", "8", "1"])

        return True

class TV(debounce_handler):
    def __init__(self):
        super(TV, self).__init__()
        self.name = "TV"
        self.port = 52002

    def act(self, client_address, state):
        print "TV: State", state, "from client @", client_address

        if (state):
            cmd(["echo", "'on", "0'", "|", "cec-client", "-s", "-d", "1"])
        else:
            cmd(["echo", "'standby", "0'", "|", "cec-client", "-s", "-d", "1"])

        return True

class Input(debounce_handler):
    def __init__(self):
        super(Input, self).__init__()
        self.name = "Input"
        self.port = 52003

    def act(self, client_address, state):
        print "Input: State", state, "from client @", client_address

        if (state):
            cmd(["echo", "'tx", "2F:82:10:00'", "|", "cec-client", "-s", "-d", "1"])
        else:
            cmd(["echo", "'tx", "2F:82:20:00'", "|", "cec-client", "-s", "-d", "1"])

        return True


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = False
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register devices
    pc = PC()
    fauxmo.fauxmo(pc.name, u, p, None, pc.port, pc)
    speaker = Speaker()
    fauxmo.fauxmo(speaker.name, u, p, None, speaker.port, speaker);
    tv = TV()
    fauxmo.fauxmo(tv.name, u, p, None, tv.port, tv);
    inp = Input()
    fauxmo.fauxmo(inp.name, u, p, None, inp.port, inp);

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
