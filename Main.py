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


    # robot.LWheel.setPower(25)
    sleep(2)
    # robot.LWheel.setSpeed(400)
    robot.LWheel.setPower(100)
    sleep(5)

    robot.close()
