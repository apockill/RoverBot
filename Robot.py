"""
    This is theoretically where the robot will collect information in real-time and record
    it all. For example, taking distance readings, reading the encoders, and more.

"""
import RoboHat
import RPi.GPIO as GPIO
from threading   import Thread, RLock
from time        import sleep, time
from collections import namedtuple

global startTime
startTime  = time()
getRunTime = lambda: time() - startTime

class RobotHandler:
    """
    Initializes and starts a thread where it loops over sensors and logs data as it comes in.
    """

    def __init__(self):
        RoboHat.init()

        self.actionLock = RLock()

        self.leftWheel = Encoder(15, 16)

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

        # In case the thread didn't close, use the lock when closing up
        with self.actionLock:
            RoboHat.cleanup()




class Encoder:
    """
    When Speed is:
        Positive
        11
        10
        00
        01
        11

        Negative
        11
        01
        00
        10
        11
    """
    LogEntry = namedtuple("LogEntry", ["A", "B", "time", "count", "vel", "acc"])

    def __init__(self, pinA, pinB):
        self.pinA  = pinA
        self.pinB  = pinB

        # This lookup table returns 1 if the motor is moving forward, 0 if backward, depending on pin logs
        #  (prev A, prev B, curr A, curc B)
        self.getDir = {(1, 1, 1, 0):  1,  # Forward direction
                       (1, 0, 0, 0):  1,
                       (0, 0, 0, 1):  1,
                       (0, 1, 1, 1):  1,
                       (1, 1, 0, 1): -1,  # Backward direction
                       (0, 1, 0, 0): -1,
                       (0, 0, 1, 0): -1,
                       (1, 0, 1, 1): -1}
        self.distancePerTick = .1  # CM

        # Set up GPIO Pins
        GPIO.setup(self.pinA, GPIO.IN)
        GPIO.setup(self.pinB, GPIO.IN)

        # Get current GPIO Values
        self.log = []  # [(pA, pB), (pA, pB)]
        firstEntry = self.LogEntry(A     = GPIO.input(self.pinA),
                                   B     = GPIO.input(self.pinB),
                                   time  = getRunTime(),
                                   count = 0,
                                   vel   = 0,
                                   acc   = 0)
        self.log.append(firstEntry)

        # Set up GPIO Events (after having gotten the values!)
        GPIO.add_event_detect(pinA, GPIO.BOTH, callback = self.pinChangeEvent, bouncetime=5)
        GPIO.add_event_detect(pinB, GPIO.BOTH, callback = self.pinChangeEvent, bouncetime=5)

    def pinChangeEvent(self, pin):
        # Find the pin that has been flipped, then act accordingly
        newPinA = self.log[-1].A
        newPinB = self.log[-1].B

        if pin == self.pinA: newPinA = int(not newPinA)
            
        if pin == self.pinB: newPinB = int(not newPinB)

        self.addLogEntry(newPinA, newPinB)


    def addLogEntry(self, newPinA, newPinB):
        """
        Generates a log entry
        :param newPinA: The  new value of pin A
        :param newPinB: The new value of pin B
        :return: True if the operation was successful. False if there was an error (aka, encoder skipped a beat)
        """
        lookup = (self.log[-1].A, self.log[-1].B, newPinA, newPinB)

        # Get direction of turn

        try:
            direction = self.getDir[lookup]
        except KeyError:
            print("Error: " + str(lookup))
            direction = 0

        currentTime = getRunTime()

        # Get the instantaneous velocity of the motor
        elapsedTime     = currentTime - self.log[-1].time
        instantVelocity = self.distancePerTick / elapsedTime

        newEntry = self.LogEntry(A     = newPinA,
                                 B     = newPinB,
                                 time  = currentTime,
                                 count = self.log[-1].count + direction,
                                 vel   = round(instantVelocity, 5),
                                 acc   = 0)
        self.log.append(newEntry)

        print(str(newEntry.A) + str(newEntry.B) + " " + str(newEntry.vel) + " \t" + elapsedTime)
