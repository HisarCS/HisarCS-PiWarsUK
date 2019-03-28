from MotorControl import MotorControl
from RemoteController import RemoteController
from time import sleep

motor = MotorControl(0, 17, 1, 27)
motor.armMotors()

cont = RemoteController()
cont.startListening()

while True:
	lx, ly = cont.getLeftJoystick()
	#print(lx, ly)
	#motor.setMotorSpeeds(70,70)
	#sleep(5)
	#motor.setMotorSpeeds(-70, -70)
	#sleep(5)
	#motor.setMotorSpeeds(0, 0)
	#sleep(5)
