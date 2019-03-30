import cv2
import imutils
from threading import Thread
from time import sleep, time
from HisarCS_PiWarsUK import MotorControl
import numpy as np


motor = MotorControl(0, 17, 1, 27)
motor.armMotors() ## OOOHHH YEAH LIGHTNING IS READY!!!!
vs = VideoStream(src=0).start()


experimental_values_of_red = (1, 2, 3)
experimental_values_of_green = (1, 2, 3)
experimental_values_of_blue = (1, 2, 3)
experimental_values_of_yellow = (1, 2, 3)


def actualColorRanges(experimental_values_of_red, experimental_values_of_green, experimental_values_of_blue, experimental_values_of_yellow):
    lowerRed = np.array([experimental_values_of_red[0] - 15, experimental_values_of_red[1] - 50, experimental_values_of_red[2] - 50], dtype = "uint8")
    lowerRed1 = np.array([0], dtype = "uint8")
    if lowerRed[0] < 0:
        lowerRed1 = np.array((abs(lowerRed[0]), experimental_values_of_red[1] - 50, experimental_values_of_red[2] - 50), dtype = "uint8")
        lowerRed[0] = 0
    upperRed = np.array((experimental_values_of_red[0] + 15, experimental_values_of_red[1] + 20, experimental_values_of_red[2] + 20), dtype = "uint8")

    lowerGreen = np.array((experimental_values_of_green[0] - 15, experimental_values_of_green[1] - 50, experimental_values_of_green[2] - 50), dtype = "uint8")
    upperGreen = np.array((experimental_values_of_green[0] + 15, experimental_values_of_green[1] + 50, experimental_values_of_green[2] + 50), dtype = "uint8")

    lowerBlue = np.array((experimental_values_of_blue[0] - 15, experimental_values_of_blue[1] - 50, experimental_values_of_blue[2] - 50), dtype = "uint8")
    upperBlue = np.array((experimental_values_of_blue[0] + 15, experimental_values_of_blue[1] + 50, experimental_values_of_blue[2] + 50), dtype = "uint8")

    lowerYellow = np.array((experimental_values_of_yellow[0] - 15, experimental_values_of_yellow[1] - 50, experimental_values_of_yellow[2] - 50), dtype = "uint8")
    upperYellow = np.array((experimental_values_of_yellow[0] + 15, experimental_values_of_yellow[1] + 50, experimental_values_of_yellow[2] - 50), dtype = "uint8")

    return lowerRed, lowerRed1, upperRed, lowerGreen, upperGreen, lowerBlue, upperBlue, lowerYellow, upperYellow


def findColor(frame, lower, upper, threshAreaValue):

    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    coloredArea = cv2.inRange(frame, lower, upper)

    (cnts, _) = cv2.findContours(coloredArea.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(coloredArea.shape[:2], dtype="uint8")
    for cnt in cnts:
        if (cv2.contourArea(cnt) > threshAreaValue):
            accuracy = 0.005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, accuracy, True)
            cv2.fillPoly(mask, [approx], 255, lineType=8, shift=0)
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
    return  cX


queue = "RGBY"

for c in queue:
    if c == "R":
        print("looking for red")
        motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.2, 0.0))
        while True:
            lower, lower1, upper, _, _, _, _, _, _ =  actualColorRanges(experimental_values_of_red,
                                                                        experimental_values_of_green,
                                                                        experimental_values_of_blue,
                                                                        experimental_values_of_yellow)
            frame = frame[1]
            if frame is None:
                break

            ### somehow get the frames

            cX = findColor(frame, lower, upper, 500)
            if cX > (frame.shape[1]/2.0 + frame.shape[1]*0.25) and cX > (frame.shape[1]/2.0 - frame.shape[1]*0.25): #if the center of the color is between 25% and 75%
                motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.0, 0.0))
                break



    if c == "G":
        print("looking for green")
        motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.2, 0.0))
        while True:
            _, _, _, lower, upper, _, _, _, _ = actualColorRanges(experimental_values_of_red,
                                                                       experimental_values_of_green,
                                                                       experimental_values_of_blue,
                                                                       experimental_values_of_yellow)
            frame = frame[1]
            if frame is None:
                break

            ### somehow get the frames

            cX = findColor(frame, lower, upper, 500)
            if cX > (frame.shape[1] / 2.0 + frame.shape[1] * 0.25) and cX > (frame.shape[1] / 2.0 - frame.shape[1] * 0.25):  # if the center of the color is between 25% and 75%
                motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.0, 0.0))
                break



    if c == "B":
        print("looking for blue")
        motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.2, 0.0))
        while True:
            _, _, _, _, _, lower, upper, _, _ = actualColorRanges(experimental_values_of_red,
                                                                       experimental_values_of_green,
                                                                       experimental_values_of_blue,
                                                                       experimental_values_of_yellow)
            frame = frame[1]
            if frame is None:
                break

            ### somehow get the frames

            cX = findColor(frame, lower, upper, 500)
            if cX > (frame.shape[1] / 2.0 + frame.shape[1] * 0.25) and cX > (frame.shape[1] / 2.0 - frame.shape[1] * 0.25):  # if the center of the color is between 25% and 75%
                motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.0, 0.0))
                break



    if c == "Y":
        print("looking for yellow")
        motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.2, 0.0))
        while True:
            _, _, _, _, _, _, _, lower, upper = actualColorRanges(experimental_values_of_red,
                                                                       experimental_values_of_green,
                                                                       experimental_values_of_blue,
                                                                       experimental_values_of_yellow)
            frame = frame[1]
            if frame is None:
                break

            ### somehow get the frames

            cX = findColor(frame, lower, upper, 500)
            if cX > (frame.shape[1] / 2.0 + frame.shape[1] * 0.25) and cX > (frame.shape[1] / 2.0 - frame.shape[1] * 0.25):  # if the center of the color is between 25% and 75%
                motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.0, 0.0))
                break


    while True:

        start = time()
        motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed((cX - frame.shape[1]/2.0)/ float(frame.shape[1]), 0.3))
        elapsed = abs(start - time())
        if elapsed > 10:
            break

    motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.0, -0.7)
    sleep(2)
    motor.setMotorSpeeds(motor.ControllerDataToMotorSpeed(0.0, 0.0)


