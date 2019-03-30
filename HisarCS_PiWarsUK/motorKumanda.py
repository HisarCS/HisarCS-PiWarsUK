from RemoteController import RemoteController
from MotorControl import MotorControl

cont = RemoteController()
motor = MotorControl(0, 17, 1, 27)

motor.armMotors()
cont.startListening()

while True:
	lx, ly = cont.getLeftJoystick()
	boost = 1
	if(6 in cont.buttons):
		boost = 0.25
	elif(7 in cont.buttons):
		boost = 2

	r, l = motor.controllerToMotor(-lx, -ly)
	motor.setMotorSpeeds(r * boost, l * boost)
