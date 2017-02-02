import RoboHat
from threading   import Thread, RLock
from time        import sleep, time
from Wheels      import Wheel





class RobotHandler:
    """
    Initializes and starts a thread where it loops over sensors and logs data as it comes in.
    """

    def __init__(self):
        RoboHat.init()

        self.actionLock = RLock()

        self.LWheel = Wheel(36, 35, 15, 16)
        # self.RWheel = Wheel(33, 32, 13, 29)

        # Threading
        self.stopThread = False
        self.mainThread = Thread(target=self.mainLoop)
        self.mainThread.start()

    def mainLoop(self):
        while not self.stopThread:
            sleep(.1)
            # self.leftWheel.update()

    def setSpeed(self, speed):
        """
        Sets both wheels
        :param speed: Positive means forward, negative means backwards, 0 means stop
        """

        with self.actionLock:
            self.LWheel.setPower(speed)
            self.RWheel.setPower(speed)

    def close(self):
        # Run this when ending the main python script
        print("Robot| Closing Thread")
        self.stopThread = True
        self.mainThread.join(2)

        # In case the thread didn't close, use the lock when closing up
        with self.actionLock:
            RoboHat.cleanup()


