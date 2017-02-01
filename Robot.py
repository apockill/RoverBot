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

        self.LWheel = Encoder(15, 16)
        self.RWheel = Encoder(13, 29)

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
    LogEntry = namedtuple("LogEntry", ["A", "B", "time", "count"])

    # State Variables
    A     = 0
    B     = 0
    time  = getRunTime()
    count = 0


    def __init__(self, pinA, pinB):
        self.pinA    = pinA
        self.pinB    = pinB


        # This lookup table returns 1 if the motor is moving forward, 0 if backward, depending on pin logs
        #  (prev A, prev B, curr A, curc B)
        self.getDir = {(1, 1, 1, 0):  1,  # Backward direction
                       (1, 0, 0, 0):  1,
                       (0, 0, 0, 1):  1,
                       (0, 1, 1, 1):  1,
                       (1, 1, 0, 1): -1,  # Forward direction
                       (0, 1, 0, 0): -1,
                       (0, 0, 1, 0): -1,
                       (1, 0, 1, 1): -1}
        self.mmPerTick = 4.83308845108  # mm

        # Set up GPIO Pins
        GPIO.setup(self.pinA, GPIO.IN)
        GPIO.setup(self.pinB, GPIO.IN)

        # DEBUG
        sleep(.2)

        # Get current GPIO Values
        self.log = []  # [(pA, pB), (pA, pB)]
        self.A = GPIO.input(self.pinA)
        self.B = GPIO.input(self.pinB)
        firstEntry = self.LogEntry(A     = self.A,
                                   B     = self.B,
                                   time  = getRunTime(),
                                   count = 0)

        self.log.append(firstEntry)

        # Set up GPIO Events (after having gotten the values!) High bouncetime causes issues.
        GPIO.add_event_detect(pinA, GPIO.BOTH, callback = self.pinChangeEvent)
        GPIO.add_event_detect(pinB, GPIO.BOTH, callback = self.pinChangeEvent)

    def pinChangeEvent(self, pin):
        # Find the pin that has been flipped, then act accordingly
        newPinA = self.A
        newPinB = self.B

        if pin == self.pinA: newPinA = GPIO.input(self.pinA)  # int(not newPinA)#
        if pin == self.pinB: newPinB = GPIO.input(self.pinB)  # int(not newPinB)#

        self.addLogEntry(newPinA, newPinB)

    def addLogEntry(self, newPinA, newPinB):
        """
        Generates a log entry
        :param newPinA: The  new value of pin A
        :param newPinB: The new value of pin B
        :return: True if the operation was successful. False if there was an error (aka, encoder skipped a beat)
        """

        # Check validity and get direction of turn
        lookup = (self.A, self.B, newPinA, newPinB)
        try:
            direction = self.getDir[lookup]
        except KeyError:
            print("Error: " + str(lookup))
            direction = 0

        # If it's not a full count (AKA 01 or 10, then skip updating the other info) then update A, B, and leave
        if not newPinA == newPinB:
            self.A = newPinA
            self.B = newPinB
            return


        # Update State Values
        self.A      = newPinA
        self.B      = newPinB
        self.time   = getRunTime()
        self.count += direction


        # Log the current State Values
        newEntry = self.LogEntry(A     = self.A,
                                 B     = self.B,
                                 time  = self.time,
                                 count = self.count)
        self.log.append(newEntry)

        print(round(self.getVelocity()), self.count, self)


    def getVelocity(self):
        sampleSize = 5
        if len(self.log) < sampleSize: sampleSize = len(self.log)


        old         = self.log[-sampleSize]
        ticks       = self.count - old.count

        if ticks == 0: return 0

        elapsedTime = getRunTime() - old.time
        timePerTick = elapsedTime / ticks
        velocity    = self.mmPerTick / timePerTick

        return velocity

