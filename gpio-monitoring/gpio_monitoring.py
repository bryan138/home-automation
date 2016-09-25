#!/usr/bin/python

import subprocess
import RPi.GPIO as GPIO

from time import sleep


def cmd(args):
    output = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = str(output.stdout.read())
    return out.split("\n")


speaker_button = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(speaker_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Wait for button input
        GPIO.wait_for_edge(speaker_button, GPIO.FALLING)

        # Button press, try to initiate spaker-control
        status = cmd(["sudo", "/etc/init.d/speaker-control.sh", "status"])
        running = False
        for line in status:
            if ("Active: " in line):
                running = "active (running)" in line
                break

        if not running:
            cmd(["sudo", "/etc/init.d/speaker-control.sh", "restart"])
            
        sleep(1)

except Exception, e:
    GPIO.cleanup()

GPIO.cleanup()


