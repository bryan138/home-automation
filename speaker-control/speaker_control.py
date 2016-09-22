#!/usr/bin/python


import os
import sys
import socket
import struct
import datetime
import subprocess
import RPi.GPIO as GPIO

from time import sleep
from datetime import datetime, time


SERVER_MAC = "74:D4:35:F3:D6:6C"
SERVER_HOST = 25

POLL_TIME = 30
TURN_ON_DELAY = 60 * 2


def host_is_up(host):
    hostname = "192.168.0." + str(host)
    response = os.system("ping -W 1 -c 1 " + hostname + " > /dev/null 2>&1")
    return (response == 0)

def wake_on_lan(macaddress):
    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        log('Incorrect MAC address format', macaddress)

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = ''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))

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


speakers = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(speakers, GPIO.OUT)


try:
    # System has been turned on, wake PC and turn on speakers
    GPIO.output(speakers, GPIO.LOW)
    wake_on_lan(SERVER_MAC)
    sleep(TURN_ON_DELAY)

    # Start monitoring PC up state
    while True:
        if host_is_up(SERVER_HOST):
            # PC is still active, sleep
            sleep(POLL_TIME)

        else:
            sleep(3)
            if not host_is_up(SERVER_HOST):
                # PC is offline, turn speakers off
                GPIO.output(speakers, GPIO.HIGH)
                break

except Exception, e:
    log("Speaker Control has been terminated", str(sys.exc_info()[0]))
    GPIO.cleanup()

GPIO.cleanup()
