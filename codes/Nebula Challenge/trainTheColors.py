import cv2
import imutils
from threading import Thread
from time import sleep
from statistics import mean
from HisarCS_PiWarsUK import OptimizedPiCamera




class VisionProcessor:

    def __init__(self):
        print("created object")
        self.isProcessing = False
        self.success = False
        self.trainingStarted = False
        self.meanHue = None
        self.meanSat = None
        self.meanVal = None
        self.frame = None


    def startVisionProcessing(self):
        self.initBB = None
        self.isProcessing = True
        self.resized = None
        self.ROI = None
        self.success = False
        self.selectingROI = False

        Thread(target=self.__visionProcessing__, args=()).start()

    def __visionProcessing__(self):

        tracker = cv2.TrackerCSRT_create()

        sleep(1)


        while self.isProcessing:

            while self.selectingROI:
                sleep(0.0001)

            # check to see if we have reached the end of the stream
            if self.frame is None:
                break

            self.resized = imutils.resize(self.frame.copy(), width=200)

            # check to see if we are currently tracking an object
            if self.initBB is not None:
                # start OpenCV object tracker using the supplied bounding box
                # coordinates, then start the FPS throughput estimator as well
                tracker.init(self.resized, self.initBB)

                # grab the new bounding box coordinates of the object
                (self.success, box) = tracker.update(self.resized)

                # check to see if the tracking was a success
                if self.success:
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(self.resized, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    self.ROI = self.resized[y:y+h, x:x+w]
                    if self.trainingStarted is False:
                        self.colorTrainerStart()


        self.isProcessing = False

    def returnValues(self):
        return self.resized, self.ROI

    def colorTrainerStart(self):
        self.trainingStarted = True
        Thread(target=self.__colorTrainer__, args=()).start()

    def __colorTrainer__(self):

        self.meanHuel = list()
        self.meanSatl = list()
        self.meanVall = list()
        self.meanHuell = list()
        self.meanSatll = list()
        self.meanValll = list()


        while self.isProcessing:
            if self.ROI is not None:
                self.hsv = cv2.cvtColor(self.ROI, cv2.COLOR_BGR2HSV)
                self.hue, self.sat, self.val = cv2.split(self.hsv)
                try:
                    for i in range(10, self.hsv.shape[0] - 10):
                        self.meanHuel.append(mean(self.hue[i]))
                        self.meanSatl.append(mean(self.sat[i]))
                        self.meanVall.append(mean(self.val[i]))

                    self.meanHuell.append(mean(self.meanHuel))
                    self.meanSatll.append(mean(self.meanSatl))
                    self.meanValll.append(mean(self.meanVall))

                    self.meanHue = mean(self.meanHuell[5: len(self.meanHuell) - 5])
                    self.meanSat = mean(self.meanSatll[5: len(self.meanSatll) - 5])
                    self.meanVal = mean(self.meanValll[5: len(self.meanValll) - 5])

                    self.meanHuel = list()
                    self.meanSatl = list()
                    self.meanVall = list()
                    self.meanHuell = list()
                    self.meanSatll = list()
                    self.meanValll = list()
                except:
                    pass
                sleep(0.05)

    def colorTrainerMeanGet(self):
        return self.meanHue, self.meanSat, self.meanVal






camera = OptimizedPiCamera()
camera.startGettingFrames()


visionProcessor = VisionProcessor()
visionProcessor.startVisionProcessing()


while visionProcessor.isProcessing:

    visionProcessor.frame = camera.getFrame()
    frame, ROI = visionProcessor.returnValues()


    if frame is not  None:
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):

            visionProcessor.selectingROI = True

            initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
            visionProcessor.initBB = initBB
            visionProcessor.selectingROI = False

        # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break
    if ROI is not None:
        try:
            cv2.imshow("ROI", ROI)
            h, s, v = visionProcessor.colorTrainerMeanGet()
            print(h, s, v)
        except:
            pass





visionProcessor.isProcessing = False
cv2.destroyAllWindows()





