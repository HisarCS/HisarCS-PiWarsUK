

def stopAll(motorControl=None, servoControl=None, camera=None, sonar=None, encoder=None, remoteController=None):
    if motorControl is not None:
        motorControl.disArm()

    if servoControl is not None:
        servoControl.initialPosition()

    if camera is not None:
        camera.disable()

    if sonar is not None:
        sonar.disable()

    if encoder is not None:
        encoder.disable()

    if remoteController is not None:
        remoteController.disable()



