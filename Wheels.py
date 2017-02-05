import RPi.GPIO  as GPIO
from collections import namedtuple
from time        import time
from Utility     import clamp, sign

# This is so that wheel logs have identicle time scales
global startTime
startTime  = time()
getRunTime = lambda: time() - startTime


class HardwareLoop:
    """
    This will help classes that are in some main loop that need an "update" function of some sort.
    They can check if it's time to run or not.
    """

    def __init__(self, delay):
        self.delay = delay
        self.lastTime = 0

    def isUpdate(self):
        """
        Check if it's time to update
        :return: True if ready, False if wait
        """
        return getRunTime() > self.lastTime + self.delay


    def Update(self):
        pass


class Wheel(HardwareLoop):
    """
    A wheel function holds an encoder object, but has the ability to
    adjust the 'speed' of the wheel. The Wheel should be run inside
    a loop, where 'update' is called every so often.

    The idea of this class is that you  can keep track of the wheel
    speed and adjust it on the fly.
    """


    def __init__(self, wheelPinA, wheelPinB, encoderPinA, encoderPinB):
        super().__init__(delay=0.1)

        # Set up Wheel Controls
        self.speed   = 0
        self.power   = 0

        # Set up Wheel Hardware
        self.encoder = Encoder(encoderPinA, encoderPinB, self.onTickUpdate)

        self.pinA = wheelPinA
        self.pinB = wheelPinB

        GPIO.setup(self.pinA, GPIO.OUT)
        self.A_PWM = GPIO.PWM(self.pinA, 20)
        self.A_PWM.start(0)

        GPIO.setup(self.pinB, GPIO.OUT)
        self.B_PWM = GPIO.PWM(self.pinB, 20)
        self.B_PWM.start(0)

    def setSpeed(self, speed):
        """
        Set the speed goal of the wheel, in mm/s
        :param speed: Speed in mm/s
        """
        self.speed = speed

        print("Wheel| Set Speed to", speed)

        # Kickstart the motor so that there's some velocity values and tick responses

        if self.power == 0:
            minUnit = 10
            if speed > 0: self.setPower(minUnit)
            if speed < 0: self.setPower(-minUnit)

    def setPower(self, power):
        """
        Set the power to the motor
        :param power: A value from 0 to 100
        """


        # Sanitize power values
        if power >  100: power = 100
        if power < -100: power = -100

        self.power = power

        # Set motor PWMs
        if power > 0:
            self.A_PWM.ChangeDutyCycle(power)
            self.B_PWM.ChangeDutyCycle(0)
            self.A_PWM.ChangeFrequency(power + 5)

        if power < 0:
            power = abs(power)
            self.A_PWM.ChangeDutyCycle(0)
            self.B_PWM.ChangeDutyCycle(power)
            self.B_PWM.ChangeFrequency(power + 5)

        if power == 0:
            self.A_PWM.ChangeDutyCycle(0)
            self.B_PWM.ChangeDutyCycle(0)

    def Update(self):
        """
        This function runs whenever the encoder on the wheel has an updated tick
        :return:
        """
        if not self.isUpdate(): return

        print(getRunTime())
        # # Constants
        # maxChange = .25
        #
        # # Get the change in power necessary
        # velocity = self.encoder.getVelocity()
        # error  = self.speed - velocity
        # change = clamp(error, -maxChange, maxChange)
        #
        # # Get the final power
        # power  = clamp(self.power + change, -100, 100)
        #
        # # Set the power
        # self.setPower(power)
        #
        #
        # # PWM CONTROL TEST BED
        # """
        # # Constants
        # kP = .04
        # maxChange = 1
        #
        # # Get the change in power necessary
        # velocity = self.encoder.getVelocity()
        # error  = self.speed - velocity
        # change = kP * error
        #
        # # Limit the change in power by maxChange
        # if abs(change) > maxChange: change = sign(change) * maxChange
        #
        # # Get the final power
        # power  = clamp(self.power + change, -100, 100)
        #
        #
        # # Set the power
        # self.setPower(power)
        # """
        # print("Error:", round(error, 3), "  Power:", round(power, 3), "  Velocity:", round(velocity, 3))

    def close(self):
        # Close main thread and close encoder events
        self.encoder.close()


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

    def __init__(self, pinA, pinB):
        """

        :param pinA: GPIO Pin for Encoder
        :param pinB: GPIO Pin for Encoder
        :param onPinUpdate: Function that will be called after any pin update
        """

        # Set up basic globals
        self.pinA = pinA
        self.pinB = pinB

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
        GPIO.add_event_detect(pinA, GPIO.BOTH, callback=self.pinChangeEvent, bouncetime=1)
        GPIO.add_event_detect(pinB, GPIO.BOTH, callback=self.pinChangeEvent, bouncetime=1)

    def pinChangeEvent(self, pin):
        # Find the pin that has been flipped, then act accordingly
        newPinA = self.A
        newPinB = self.B

        if pin == self.pinA: newPinA = GPIO.input(self.pinA)  # int(not newPinA)#
        if pin == self.pinB: newPinB = GPIO.input(self.pinB)  # int(not newPinB)#


        # Check validity and get direction of turn
        lookup = (self.A, self.B, newPinA, newPinB)
        try:
            direction = self.getDir[lookup]
        except KeyError:
            print("Encoder| ERROR during lookup: " + str(lookup))
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

        # Run the Callback Function for the parent
        self.getVelocity()

    def getVelocity(self):
        sampleSize = 3
        if len(self.log) < sampleSize + 1: sampleSize = len(self.log)

        old = self.log[-sampleSize]
        ticks = self.count - old.count

        if ticks == 0: return 0

        time        = getRunTime()
        elapsedTime = time - old.time
        timePerTick = elapsedTime / ticks
        velocity    = self.mmPerTick / timePerTick

        # print("P", str(self.A)+str(self.B), "C", self.count, "T", round(time, 2), "V", round(velocity, 2), "Old", old)

        return velocity

    def close(self):
        GPIO.remove_event_detect(self.pinA)
        GPIO.remove_event_detect(self.pinB)

