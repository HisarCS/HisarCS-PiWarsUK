from RemoteController import RemoteController
from MotorControl import MotorControl

cont = RemoteController()

cont.startListening()

while True:
	lx, ly = cont.getLeftJoystick()
	print(lx, ly)