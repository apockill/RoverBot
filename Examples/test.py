import time, sys
import RPi.GPIO as GPIO
import RoboHat

wheelEnc  = 15
wheelEnc2 = 16
RoboHat.init()
GPIO.setup( wheelEnc, GPIO.IN)
GPIO.setup(wheelEnc2, GPIO.IN)
speed = 10

RoboHat.forward(speed)
try:
    while True:
        print('Reading ' + str(GPIO.input(wheelEnc)) + ' ' + str(GPIO.input(wheelEnc2)))
        time.sleep(.05)
         

except KeyboardInterrupt:
        print('Shutting Down')
    
RoboHat.cleanup()
