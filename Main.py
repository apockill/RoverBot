from time import sleep

import cv2
import Constants as Const
from HardwareLibs.Rover import RoverHandler
from HardwareLibs.Camera import PanTiltPiCamera

if __name__ == "__main__":
    robot  = RoverHandler()


    # print("Final L: ", robot.LWheel.encoder.getVelocity(sampleSize=50))
    # print("Final R: ", robot.RWheel.encoder.getVelocity(sampleSize=50))
    robot.close()

