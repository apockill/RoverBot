from threading import Thread, RLock
from time import sleep

import Constants as Const
from Behaviors import FollowLine
from HardwareLibs import RoboHat
from HardwareLibs.Camera import PanTiltPiCamera
from HardwareLibs.Wheel import Wheel


class RoverHandler:
    """
    Initializes and starts a thread where it loops over sensors and logs data as it comes in.
    """

    def __init__(self):
        RoboHat.init()

        self.actionLock = RLock()

        # Hardware
        self.LWheel = Wheel(Const.leftWheelPinA,
                            Const.leftWheelPinB,
                            Const.leftEncoderPinA,
                            Const.leftEncoderPinB)

        self.RWheel = Wheel(Const.rightWheelPinA,
                            Const.rightWheelPinB,
                            Const.rightEncoderPinA,
                            Const.rightEncoderPinB)

        self.camera = PanTiltPiCamera(Const.cameraPanPin, Const.cameraTiltPin)

        # Behaviors
        self.behavior = FollowLine(self)

        # Threading
        self.stopped = False
        # self.mainThread = Thread(target=self.mainThread)
        # self.mainThread.start()

    def mainThread(self):
        while not self.stopped:
            sleep(.0001)
            with self.actionLock:
                # Do Hardware Updates
                self.LWheel.update()
                self.RWheel.update()

                # Do Behavior Updates
                self.behavior.update()

            self.stopped = True
        self.close()

    def setMoveRadius(self, speed, radius):
        """
        Sets both wheels
        :param speed: Positive means forward, negative means backwards, 0 means stop
        """

        if radius == 0: return

        vL = speed * (1 + Const.distBetweenWheels / (2 * radius))
        vR = speed * (1 - Const.distBetweenWheels / (2 * radius))

        print("vL ", vL, "\tvR", vR)

        with self.actionLock:
            self.LWheel.setSpeed(vL)
            self.RWheel.setSpeed(vR)

    def close(self):
        # Run this when ending the main python script
        print("Robot| Closing Robot Thread")

        # Safely close main threads
        # self.stopped = True
        # self.mainThread.join(2)


        # In case the thread didn't close, use the lock when closing up
        with self.actionLock:
            self.LWheel.close()
            self.RWheel.close()
            self.camera.close()

            RoboHat.cleanup()


