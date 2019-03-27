
from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread
import cv2

class OptimizedPiCamera:

    def __init__(self, resolution=(640, 480)):

        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.rawFrame = PiRGBArray(self.camera, size=self.camera.resolution)
        self.cameraStream = self.camera.capture_continuous(self.rawFrame, format="bgr", use_video_port=True)
        self.currentFrame = None

        self.framesToShow = dict()
        self.isWindowShowEnabled = False

    def startGettingFrames(self):

        Thread(target=self.__updateFrame__, args=()).start()
        return self

    def __updateFrame__(self):

        for frame in self.cameraStream:

            self.currentFrame = frame.array
            self.rawFrame.truncate(0)

    def getFrame(self):

        return self.currentFrame

    def showFrame(self, windowName="frame", frameToShow=None):
        if frameToShow is None:
            self.framesToShow[windowName] = self.currentFrame
        else:
            self.framesToShow[windowName] = frameToShow

        if not self.isWindowShowEnabled:
            Thread(target=self.__updateWindowFrame__, args=()).start()
            self.isWindowShowEnabled = True


    def __updateWindowFrame__(self):

        while self.isWindowShowEnabled:

            for name in self.framesToShow.copy():
                cv2.imshow(name, self.framesToShow[name])

            key = cv2.waitKey(1)

            if key == ord("q"):
                cv2.destroyAllWindows()
                break

    def disableCamera(self):
        picamera.closed()

    def closeAllWindows(self):
        self.isWindowShowEnabled = False

