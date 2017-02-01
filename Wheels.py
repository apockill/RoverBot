import RPi.GPIO as GPIO
from collections import namedtuple
from time import time

# This is so that wheel logs have identicle time scales
global startTime
startTime  = time()
getRunTime = lambda: time() - startTime



class Wheel:
    """
    A wheel function holds an encoder object, but has the ability to
    adjust the 'speed' of the wheel whenever the encoder receives a
    new tick. Thus you can keep track of the wheel speed and adjust
    it on the fly.
    """

    def __init__(self, pinA, pinB):
        self.encoder = Encoder(pinA, pinB, self.onTickUpdate)
        self.speed = 0

    def setSpeed(self, speed):
        """
        Set the speed goal of the wheel, in mm/s
        :param speed: Speed in mm/s
        """
        self.speed = speed

    def onTickUpdate(self):
        """
        This function runs whenever the encoder on the wheel has an updated tick
        :return:
        """
        print("Got update")

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
    A = 0
    B = 0
    time = getRunTime()
    count = 0

    def __init__(self, pinA, pinB, onPinUpdate):
        """

        :param pinA: GPIO Pin for Encoder
        :param pinB: GPIO Pin for Encoder
        :param onPinUpdate: Function that will be called after any pin update
        """

        # Set up basic globals
        self.pinA        = pinA
        self.pinB        = pinB
        self.onPinUpdate = onPinUpdate

        # This lookup table returns 1 if the motor is moving forward, 0 if backward, depending on pin logs
        #  (prev A, prev B, curr A, curc B)
        self.getDir = {(1, 1, 1, 0): 1,  # Backward direction
                       (1, 0, 0, 0): 1,
                       (0, 0, 0, 1): 1,
                       (0, 1, 1, 1): 1,
                       (1, 1, 0, 1): -1,  # Forward direction
                       (0, 1, 0, 0): -1,
                       (0, 0, 1, 0): -1,
                       (1, 0, 1, 1): -1}
        self.mmPerTick = 4.83308845108  # mm

        # Set up GPIO Pins
        GPIO.setup(self.pinA, GPIO.IN)
        GPIO.setup(self.pinB, GPIO.IN)

        # Get current GPIO Values
        self.log = []  # [(pA, pB), (pA, pB)]
        self.A = GPIO.input(self.pinA)
        self.B = GPIO.input(self.pinB)
        firstEntry = self.LogEntry(A=self.A,
                                   B=self.B,
                                   time=getRunTime(),
                                   count=0)

        self.log.append(firstEntry)

        # Set up GPIO Events (after having gotten the values!) High bouncetime causes issues.
        GPIO.add_event_detect(pinA, GPIO.BOTH, callback=self.pinChangeEvent)
        GPIO.add_event_detect(pinB, GPIO.BOTH, callback=self.pinChangeEvent)

    def pinChangeEvent(self, pin):
        # Find the pin that has been flipped, then act accordingly
        newPinA = self.A
        newPinB = self.B

        if pin == self.pinA: newPinA = GPIO.input(self.pinA)  # int(not newPinA)#
        if pin == self.pinB: newPinB = GPIO.input(self.pinB)  # int(not newPinB)#

        self.addLogEntry(newPinA, newPinB)
        self.onPinUpdate()

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
        self.A = newPinA
        self.B = newPinB
        self.time = getRunTime()
        self.count += direction

        # Log the current State Values
        newEntry = self.LogEntry(A=self.A,
                                 B=self.B,
                                 time=self.time,
                                 count=self.count)
        self.log.append(newEntry)

        print(round(self.getVelocity()), self.count, self)

    def getVelocity(self):
        sampleSize = 5
        if len(self.log) < sampleSize: sampleSize = len(self.log)

        old = self.log[-sampleSize]
        ticks = self.count - old.count

        if ticks == 0: return 0

        elapsedTime = getRunTime() - old.time
        timePerTick = elapsedTime / ticks
        velocity = self.mmPerTick / timePerTick

        return velocity

