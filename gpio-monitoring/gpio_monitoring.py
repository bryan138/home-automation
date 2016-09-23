#!/usr/bin/python

import subprocess
import RPi.GPIO as GPIO

from time import sleep


def cmd(args):
    output = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = str(output.stdout.read())
    return out.split("\n")


def speaker_button_pressed():
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

speaker_button = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(speaker_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Wait for button input
        GPIO.wait_for_edge(speaker_button, GPIO.FALLING)

        speaker_button_pressed()
        sleep(1)

except Exception, e:
    GPIO.cleanup()


GPIO.cleanup()


