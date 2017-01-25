import time, sys
import RPi.GPIO as GPIO
import robohat

wheelEnc  = 15
wheelEnc2 = 16
robohat.init()
GPIO.setup( wheelEnc, GPIO.IN)
GPIO.setup(wheelEnc2, GPIO.IN)
speed = 10

robohat.forward(speed)
try:
    while True:
        print('Reading ' + str(GPIO.input(wheelEnc)) + ' ' + str(GPIO.input(wheelEnc2)))
        time.sleep(.05)
         

except KeyboardInterrupt:
        print('Shutting Down')
    
robohat.cleanup()
