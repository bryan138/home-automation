import sys
import RPi.GPIO as GPIO


pin = int(sys.argv[1])
state = int(sys.argv[2])

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
