from time import sleep

import cv2
import Constants as Const
from HardwareLibs.Rover import RoverHandler
from HardwareLibs.Camera import PanTiltPiCamera

if __name__ == "__main__":
    print("\n\nStarting!\n")
    robot  = RoverHandler()
    robot.mainThread()
    robot.LWheel.setSpeed(250)
    # print("Final L: ", robot.LWheel.encoder.getVelocity(sampleSize=50))
    # print("Final R: ", robot.RWheel.encoder.getVelocity(sampleSize=50))

