#!/usr/bin/python

import subprocess
import RPi.GPIO as GPIO

from time import sleep


def cmd(args):
    output = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = str(output.stdout.read())
    return out.split("\n")

def callback_a(channel):
    # Button press, try to initiate spaker-control
    status = cmd(["sudo", "systemctl", "status", "speaker-control"])
    running = False
    for line in status:
        if ("Active: " in line):
            running = "active (running)" in line
            break

    if not running:
        print("Start it")
        cmd(["sudo", "systemctl", "restart", "speaker-control"])
    else:
        print("already running")
    return

def callback_c(channel):
    print("C")
    return

def callback_d(channel):
    print("D")
    return

def callback_e(channel):
    print("E")
    return

def callback_f(channel):
    print("F")
    return


pins = [3, 11, 13, 15, 19]
callbacks = [callback_a, callback_c, callback_d, callback_e, callback_f]

GPIO.setmode(GPIO.BOARD)

for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin, callback in zip(pins, callbacks):
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback, bouncetime=300)

try:
    while True:
        sleep(1e6)

except Exception, e:
    GPIO.cleanup()

GPIO.cleanup()
