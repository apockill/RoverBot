from time import sleep

import cv2
import Constants as Const
from HardwareLibs.Rover import RoverHandler
from HardwareLibs.Camera import PanTiltPiCamera

if __name__ == "__main__":
    robot   = RoverHandler()

    camera = PanTiltPiCamera(Const.cameraPanPin, Const.cameraTiltPin)
    camera.start()
    camera.setPose(0, 0)

    cv2.imshow('frame', camera.read())
    cv2.waitKey(1)
    # robot.setMoveRadius(150, -150)
    # robot.setMoveRadius(200, 500)
    # robot.LWheel.setSpeed(250)
    # test

    sleep(3)
    # print("Final L: ", robot.LWheel.encoder.getVelocity(sampleSize=50))
    # print("Final R: ", robot.RWheel.encoder.getVelocity(sampleSize=50))
    robot.close()
    camera.close()
