
from __future__ import division
import time
import RPi.GPIO as GPIO


# Import the PCA9685 module.
import Adafruit_PCA9685

GPIO.setmode(GPIO.BCM)
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()


# Set frequency to 1000hz, good for servos.
pwm.set_pwm_freq(1000)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


while True:
    # Move servo on channel O between extremes.
    value = input("please enter a value:")
    pwm.set_pwm(0, 0, abs(int(value)))
    pwm.set_pwm(1, 0, abs(int(value)))

    if int(value) < 0:
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
    if int(value) > 0:
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
