import RoboHat
import Constants
from Utility     import clamp
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

        # Hardware
        self.LWheel = Wheel(33, 32, 15, 16)
        self.RWheel = Wheel(36, 35, 13, 29)

        # Threading
        self.stopThread = False
        self.mainThread = Thread(target=self.mainLoop)
        self.mainThread.start()

    def mainLoop(self):
        while not self.stopThread:
            sleep(.0001)
            with self.actionLock:
                pass
                # self.LWheel.Update()
                # self.RWheel.Update()

    def setMoveRadius(self, speed, radius):
        """
        Sets both wheels
        :param speed: Positive means forward, negative means backwards, 0 means stop
        """

        if radius == 0: return

        vL = speed * (1 + Constants.distBetweenWheels / (2 * radius))
        vR = speed * (1 - Constants.distBetweenWheels / (2 * radius))

        print("vL ", vL, "\tvR", vR)

        with self.actionLock:
            self.LWheel.setPower(vL)
            self.RWheel.setPower(vR)

    def close(self):
        # Run this when ending the main python script
        print("Robot| Closing Thread")

        # Safely close main threads
        self.stopThread = True
        self.mainThread.join(2)

        # In case the thread didn't close, use the lock when closing up
        with self.actionLock:
            self.LWheel.close()
            self.RWheel.close()
            RoboHat.cleanup()


