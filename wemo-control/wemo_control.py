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
SERVER_IP = "192.168.0.25"


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
        print "State", state, "from client @", client_address

        if (state):
            # Check if speaker_control service is running
            status = cmd(["sudo", "/etc/init.d/speaker-control.sh", "status"])
            running = False
            for line in status:
                if ("Active: " in line):
                    if "active (running)" in line:
                        running = True
                    break

            if not running:
                cmd(["sudo", "/etc/init.d/speaker-control.sh", "restart"])

        else:
            cmd(["net", "rpc", "shutdown", "-t", "30", "-I", SERVER_IP, "-U", USERNAME + "%" + PASSWORD])

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