from Aadafruit_servokit import *


class ServoControl:

    def __init__(self, channel):

        self.channel = channel
        self.kit = ServoKit(self.channel)

    def setServoAngle(self, angle):
        self.angle = angle
        self.kit.servo[0].angle = self.angle

    def initialPosition(self):
        self.kit.servo[0].angle = 90

