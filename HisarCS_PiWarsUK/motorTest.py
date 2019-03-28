from MotorControl import MotorControl
from time import sleep
import RPi.GPIO as GPIO

motor = MotorControl(0, 17, 1, 27)
motor.armMotors()

motor.setMotorSpeeds(70,70)
sleep(5)
motor.setMotorSpeeds(-70, -70)
sleep(5)
motor.setMotorSpeeds(0, 0)
sleep(5)
