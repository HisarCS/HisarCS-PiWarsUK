from Aadafruit_servokit import *
import RPi.GPIO as GPIO
import pygame



class MotorControl:

    def __init__(self, rightChannel, rightDIR, leftChannel, leftDIR, GPIONumbering=GPIO.BOARD):

        self.rightChannel = rightChannel
        self.leftChannel = leftChannel
        self.GPIONumbering = GPIONumbering
        self.rightDIR = rightDIR
        self.leftDIR = leftDIR

        GPIO.setmode(GPIONumbering)

        self.rightMotor = ServoKit(self.rightChannel)
        self.leftMotor = ServoKit(self.leftChannel)

        GPIO.setup(rightDIR, GPIO.OUT)
        GPIO.setup(leftDIR, GPIO.OUT)

        self.isArmed = False


        self.rightMotor.servo[0].angle = 0
        self.leftMotor.servo[0].angle = 0

    def armMotors(self):
        pygame.init()
        HeyLightningYouReady = pygame.mixer.Sound("sounds/HeyLightningYouReady.wav")
        HeyLightningYouReady.play()
        self.isArmed = True

    def disArm(self):
        self.isArmed = False


    def setMotorSpeeds(self, rightMotorSpeed, leftMotorSpeed, turbo=False):

        self.turbo = turbo

        if self.isArmed is True:

            self.rightMotorSpeed = rightMotorSpeed
            self.leftMotorSpeed = leftMotorSpeed

            if self.rightMotorSpeed > 0:
                GPIO.output(self.rightDIR, GPIO.HIGH)
            else:
                GPIO.output(self.rightDIR, GPIO.LOW)

            if self.leftMotorSpeed > 0:
                GPIO.output(self.rightDIR, GPIO.HIGH)
            else:
                GPIO.output(self.rightDIR, GPIO.LOW)

            if self.turbo:
                self.rightMotor.servo[0].angle = abs(self.rightMotorSpeed) / 1.80
                self.leftMotor.servo[0].angle = abs(self.leftMotorSpeed) / 1.80

            if not self.turbo:
                self.rightMotor.servo[0].angle = abs(self.rightMotorSpeed) / 1.44
                self.leftMotor.servo[0].angle = abs(self.leftMotorSpeed) / 1.44

        else:
            self.rightMotor.servo[0].angle = 0
            self.leftMotor.servo[0].angle = 0
            print(" You need to arm the motors first!!! ")
