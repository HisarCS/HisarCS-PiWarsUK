import cv2
import imutils
import numpy as np
import math
from scipy import stats
import time
from HisarCS_PiWarsUK import OptimizedPiCamera
from HisarCS_PiWarsUK import MotorControl



def visionProcessing(frame, contourThreshValue, colorThreshValue, colorThreshMethod=cv2.THRESH_BINARY_INV):


    def contourOperations(thresh, threshValue):

        mask = np.zeros(thresh.shape[:2], dtype="uint8")

        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in cnts:

            if (cv2.contourArea(cnt) > threshValue):
                accuracy = 0.005 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, accuracy, True)
                cv2.fillPoly(mask, [approx], 255, lineType=8, shift=0)



        return mask, cnts

    def findOnesFromTwoSides(image, yValue):

        fromTheLeftPoint = (0,0)
        fromTheRightPoint = (0,0)

        movingPixelIndexer = 0


        # print("starting from the left, until it finds pixel value 255")

        while not (fromTheLeftPoint == 0):

            pixelIntensityValue = image[yValue, movingPixelIndexer]

            movingPixelIndexer += 1

            if pixelIntensityValue == 255:
                fromTheLeftPoint = (movingPixelIndexer, yValue)
                break

        # print("then from the right, until it finds pixel value 255")

        tempLeft = movingPixelIndexer

        movingPixelIndexer = image.shape[1] - 1

        while not (fromTheRightPoint == 0):

            pixelIntensityValue = image[yValue, movingPixelIndexer]

            movingPixelIndexer -= 1

            if pixelIntensityValue == 255:
                fromTheRightPoint = (movingPixelIndexer, yValue)
                break

        tempRight = movingPixelIndexer

        centerpoint = (int((tempRight - tempLeft) / 2 + tempLeft), yValue)

        return fromTheLeftPoint, fromTheRightPoint, centerpoint

    def percentageToPixel(pixelLength, percentage):
        return int(pixelLength * (percentage/100))


    ######################       IMAGE PROCESSING STARTING       ########################

    ######################       THRESHOLDING STUFF       ########################
    Guassian_blurred = cv2.GaussianBlur(frame.copy(), (7,7), 0)
    (T, thresh) = cv2.threshold(Guassian_blurred, colorThreshValue, 255, colorThreshMethod) # bu beyaz uzerine siyah cizgileri takip eder. Bu yuzden yarisma esnasinda 4. parametreyi "cv2.THRESH_BINARY" yapip 2. parametreyi 200 gibi bir sayi yapmaniz gerekiyor
    binaryImage, _= contourOperations(thresh, contourThreshValue)
    binaryImagePLT = cv2.flip(imutils.rotate(binaryImage.copy(), 180), 1)

    ######################       FINDING THE CRITICAL POINTS       ########################

    centerX = list()
    centerY = list()

    for criticalPoints in range(10, 50, 5):
        pointLeft, pointRight, centerPoint = findOnesFromTwoSides(binaryImagePLT, percentageToPixel(binaryImagePLT.shape[0], criticalPoints))

        cv2.circle(binaryImagePLT, pointLeft, 3, 128, -1)
        cv2.circle(binaryImagePLT, pointRight, 3, 128, -1)
        cv2.circle(binaryImagePLT, centerPoint, 3, 64, -1)

        centerY.append(centerPoint[0])
        centerX.append(centerPoint[1])

    ######################       FINDING THE SLOPE AND CALCULATING THE ERROR IN DEGREES      ########################

    inverseSlope, _, _, _, _  = stats.linregress(centerX, centerY)
    slope = 1/inverseSlope

    if (slope > 0):
        error = 90 - math.atan(slope) * 180 / 3.1415
    else:
        error = (90 + math.atan(slope) * 180 / 3.1415) * (-1)

    ######################       RETURNING THE WANTED VARIABLES       ########################

    return slope, error, cv2.flip(imutils.rotate(binaryImagePLT, 180), 1)

vs = cv2.VideoCapture(0)
motor = MotorControl(0, 17, 1, 27)


# frame = cv2.imread('/Users/yasaridikut/PycharmProjects/linefollowpiwar/IMG_7581.jpg', 0)
# frame = imutils.resize(frame, width=240)
#for the purposes of debugging/developing the code in the while loop

print("about to start the code!!")
motor.armMotors() ## OOOHHH YEAH LIGHTNING IS READY!!!!

while True:
    start = time.time()
    frame = vs.read()


    slope, error, resultFrame = visionProcessing(frame, 600, 90, cv2.THRESH_BINARY_INV) # bu beyaz uzerine siyah cizgileri takip eder. Bu yuzden yarisma esnasinda 4. parametreyi "cv2.THRESH_BINARY" yapip 2. parametreyi 200 gibi bir sayi yapmaniz gerekiyor

    elapsed = abs(start - time.time())
    print(slope, error, 1/elapsed)

    cv2.imshow("frame", frame)
    cv2.imshow("resultant Frame", resultFrame)

    if cv2.waitKey(1) == ord("q"):
        break

    ######################       SETTING THE MOTOR SPEEDS       ########################

    yAxisJoy = 0.7 #speed throughout the challenge
    xAxisJoy = (-error / 90.0) * 2 # error degree is 90 degrees when the robot can't see the line. So the variable is divided by 90.0 for float. But multiplied by 2 for better response to the error by robot.

    motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(xAxisJoy, yAxisJoy))



#for the purposes of debugging/developing the code for one cycle

#
# ######################       IMAGE PRE-PROCESSING        ########################
#
# line1 = cv2.imread('/Users/yasaridikut/PycharmProjects/linefollowpiwar/IMG_7581.jpg', 0)
#
# line1 = imutils.resize(line1, width=240)
#
# ######################       IMAGE PRE-PROCESSING DONE, THE REAL ONE IS BEGINNING       ########################
#
# start = time.time()
#
# slope, error, resultFrame = visionProcessing(line1, 600, 90, cv2.THRESH_BINARY_INV)
#
# elapsed = abs(start - time.time())
#
# print(slope, error, elapsed)
#
#
# ######################       display       ########################
#
#
# cv2.imshow('line1', line1)
#
# cv2.imshow("resultant Frame", resultFrame)
#
# cv2.waitKey(0)
#
# cv2.destroyAllWindows()
#
