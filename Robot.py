"""
    This is theoretically where the robot will collect information in real-time and record
    it all. For example, taking distance readings, reading the encoders, and more.

"""
import RoboHat
import RPi.GPIO as GPIO
from threading import Thread, RLock
from time      import sleep



class RobotHandler:
    """
    Initializes and starts a thread where it loops over sensors and logs data as it comes in.
    """

    def __init__(self):
        RoboHat.init()

        self.actionLock = RLock()

        self.leftWheel = Encoder(15, 16)

        # Threading globals
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
            
        print("Total errors: " + str(self.leftWheel.errors))



class Encoder:
    def __init__(self, pin1, pin2):
        self.pin1  = pin1
        self.pin2  = pin2
        self.count = 0  # Turn counts

        self.last   = 1  # Which pin triggered last
        self.errors = 0
        
        GPIO.setup(self.pin1, GPIO.IN)
        GPIO.setup(self.pin2, GPIO.IN)
        
        self.pin1Last = GPIO.input(self.pin1)
        self.pin2Last = GPIO.input(self.pin2)
         
        GPIO.add_event_detect(pin1, GPIO.BOTH, callback = self.pinChangeEvent, bouncetime=5)
        GPIO.add_event_detect(pin2, GPIO.BOTH, callback = self.pinChangeEvent, bouncetime=5)
        
    def pinChangeEvent(self, pin):
        if pin == self.pin1:
            self.pin1Last = int(not self.pin1Last)
            if self.last == 1:
                print ("ERROR 1")
                self.errors += 1
            self.last = 1
            
            print("A: " + str(self.pin1Last) + " " + str(self.pin2Last))
            
        elif pin == self.pin2:
            self.pin2Last = int(not self.pin2Last)
            if self.last == 2:
                print("ERROR 2")
                self.errors += 1
                
            self.last = 2
            
            print("B: " + str(self.pin1Last) + " " + str(self.pin2Last))


    def update(self):
        sleep(.01)
        pin1 = GPIO.input(self.pin1)
        sleep(.01)
        pin2 = GPIO.input(self.pin2)

        if pin1 != self.pin1Last and pin2 != self.pin2Last:
            self.pin1Last = pin1
            self.pin2Last = pin2
            print("Next: " + str(pin1) + " " + str(pin2))

    

