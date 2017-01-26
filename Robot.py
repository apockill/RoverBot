"""
    This is theoretically where the robot will collect information in real-time and record
    it all. For example, taking distance readings, reading the encoders, and more.

"""
import RoboHat
from threading import Thread, RLock
from time      import sleep


class RobotHandler:
    """
    Initializes and starts a thread where it loops over sensors and logs data as it comes in.
    """

    def __init__(self):
        RoboHat.init()

        self.actionLock = RLock()


        # Threading globals
        self.stopThread = False
        self.mainThread = Thread(target=self.mainLoop)
        self.mainThread.start()


    def mainLoop(self):

        while not self.stopThread:
            sleep(1)
            print("RobotHandler Running")

    def setSpeed(self, speed):
        """
        Sets both wheels
        :param speed: Positive means forward, negative means backwards, 0 means stop
        """
        if speed > 0:
            RoboHat.forward(abs(speed))
        if speed < 0:
            RoboHat.reverse(abs(speed))
        if speed == 0:
            RoboHat.stop()


    def close(self):
        # Run this when ending the main python script
        print("Robot| Closing Thread")
        self.stopThread = True
        self.mainThread.join(2)
        RoboHat.cleanup()



class Encoder:
    def __init__(self, pin1, pin2):
        pass

