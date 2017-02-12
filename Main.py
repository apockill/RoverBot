"""
Project Brainstorming

Hardware:
    - PWM 

Goals:
    Track lines using vision and map the nodes as it moves along
        - Move (Wheels)
        - Measure Distance (encoders)
        - Video Feed
        - Computer Vision
        -
"""

from Robot  import RobotHandler
from Video  import PiVideoStream
from time   import sleep
import cv2

if __name__ == "__main__":
    robot   = RobotHandler()

    vStream = PiVideoStream()
    vStream.start()


    cv2.imshow('frame', vStream.read())
    cv2.waitKey(1)
    # robot.setMoveRadius(150, -150)
    # robot.setMoveRadius(200, 500)
    # robot.LWheel.setSpeed(250)
    # test

    sleep(3)
    # print("Final L: ", robot.LWheel.encoder.getVelocity(sampleSize=50))
    # print("Final R: ", robot.RWheel.encoder.getVelocity(sampleSize=50))
    robot.close()
    vStream.close()
