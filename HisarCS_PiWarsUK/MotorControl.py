import Adafruit_PCA9685
import RPi.GPIO as GPIO
import board
import pygame
import math



class MotorControl:

    def __init__(self, rightChannel, rightDIR, leftChannel, leftDIR, GPIONumbering=GPIO.BCM):

        self.rightChannel = rightChannel
        self.leftChannel = leftChannel
        self.GPIONumbering = GPIONumbering
        self.rightDIR = rightDIR
        self.leftDIR = leftDIR
        
        GPIO.setmode(GPIONumbering)
        
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(1000)
        
        GPIO.setup(rightDIR, GPIO.OUT)
        GPIO.setup(leftDIR, GPIO.OUT)
       
        self.isArmed = False


        #self.kit.servo[self.rightChannel].angle = 0
        #self.kit.servo[self.leftChannel].angle = 0

    def armMotors(self):
        #pygame.init()
        #HeyLightningYouReady = pygame.mixer.Sound("sounds/HeyLightningYouReady.wav")
        #HeyLightningYouReady.play()
        self.isArmed = True

    def disArm(self):
        self.isArmed = False


    def controllerToMotor(self, x, y):
        r = math.hypot(x, y)
        t = math.atan2(y, x)

        t += math.pi / 4
        left = r * math.cos(t) * math.sqrt(2)
        right = r * math.sin(t) * math.sqrt(2)

        left = max(-1, min(left, 1))
        right = max(-1, min(right, 1))

        return int(left * 50), -int(right * 50)

    def setMotorSpeeds(self, rightMotorSpeed, leftMotorSpeed, turbo=False):

        self.turbo = turbo

        if self.isArmed is True:

            self.rightMotorSpeed = rightMotorSpeed
            self.leftMotorSpeed = leftMotorSpeed

            if int(self.leftMotorSpeed) > 0:
                GPIO.output(self.leftDIR, GPIO.HIGH)
                print("right motors forward")
            else:
                GPIO.output(self.leftDIR, GPIO.LOW)
                print("right motors backwards")

            if int(self.rightMotorSpeed) > 0:
                GPIO.output(self.rightDIR, GPIO.HIGH)
                print("left motors forward")
            else:
                GPIO.output(self.rightDIR, GPIO.LOW)
                print("left motors backwards")

            if self.turbo:
                self.pwm.set_pwm(self.rightChannel, 0, abs(int(self.rightMotorSpeed*40.95)))
                self.pwm.set_pwm(self.leftChannel, 0, abs(int(self.leftMotorSpeed*40.95)))

            if not self.turbo:
               self.pwm.set_pwm(self.rightChannel, 0, abs(int(self.rightMotorSpeed*40.95*0.8)))
               self.pwm.set_pwm(self.leftChannel, 0, abs(int(self.leftMotorSpeed*40.95*0.8)))
               print("set the pwm values:{} {}".format(self.rightMotorSpeed, self.leftMotorSpeed))
        else:
            self.pwm.set_pwm(self.rightChannel, 0, 0)
            self.pwm.set_pwm(self.leftChannel, 0, 0)
            print(" You need to arm the motors first!!! ")
