import HisarCSPiWars2019 as hp
from time import sleep

motors = hp.MotorControl()
servo = hp.ServoControl()
ultra = hp.UltrasonicSensor()

servo.setToNotContinuous()
servo.setAngle(90)

def turnRight():
	motors.setSpeeds(240, -240)
	sleep(0.4)

def turnLeft()
	motors.setSpeeds(-240, 240)
	sleep(0.4)

while True:
	dist = ultra.getDistance()

	if(dist < 7):
		servo.setAngle(0)
		rightDist = ultra.getDistance()
		servo.setAngle(180)
		leftDist = ultra.getDistance()
		if(rightDist > leftDist):
			turnRight()
		else:
			turnLeft()
	motors.setSpeeds(480, 480)
