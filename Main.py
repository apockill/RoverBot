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

from Robot import RobotHandler

from time import sleep
# import Video

if __name__ == "__main__":
    robot = RobotHandler()


    robot.setMoveRadius(250, 150)
    # robot.setMoveRadius(200, 500)
    # robot.LWheel.setSpeed(250)
    # test

    sleep(10)
    print("Final L: ", robot.LWheel.encoder.getVelocity(sampleSize=50))
    print("Final R: ", robot.RWheel.encoder.getVelocity(sampleSize=50))
    robot.close()
