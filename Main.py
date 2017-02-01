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

    robot.setSpeed(100)
    sleep(.1)
    robot.setSpeed(-100)
    sleep(.3)
    robot.setSpeed(100)
    sleep(.5)
    robot.setSpeed(-100)
    sleep(.3)
    robot.setSpeed(100)
    sleep(.1)

    robot.close()
