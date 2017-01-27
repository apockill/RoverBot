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

if __name__ == "__main__":
    robot = RobotHandler()

    for i in range(0, 100):
        
        robot.setSpeed(i)
        sleep(.1)
        
    sleep(1)


    robot.close()
