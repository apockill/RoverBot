# initio Motor Test using RoboHAT
# This uses the GPIO pins in "raw", ie. without using the library
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# Writes directly to motors without using the library
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTesta.py


import time, RPi.GPIO as gpio

#Motors
L1 = 36
L2 = 35
R1 = 33
R2 = 32

gpio.setmode(gpio.BOARD)
gpio.setup(L1, gpio.OUT)
gpio.setup(L2, gpio.OUT)
gpio.setup(R1, gpio.OUT)
gpio.setup(R2, gpio.OUT)


def forward():
    gpio.output(L1, 1)
    gpio.output(L2, 0)
    gpio.output(R1, 1)
    gpio.output(R2, 0)

def reverse():
    gpio.output(L1, 0)
    gpio.output(L2, 1)
    gpio.output(R1, 0)
    gpio.output(R2, 1)

def spinLeft():
    gpio.output(L1, 0)
    gpio.output(L2, 1)
    gpio.output(R1, 1)
    gpio.output(R2, 0)

def spinRight():
    gpio.output(L1, 1)
    gpio.output(L2, 0)
    gpio.output(R1, 0)
    gpio.output(R2, 1)

def stop():
    gpio.output(L1, 0)
    gpio.output(L2, 0)
    gpio.output(R1, 0)
    gpio.output(R2, 0)

print "Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat"
print "Press Ctrl-C to stop"
print

# main loop
try:
    while True:
        forward()
        print 'Forward'
        time.sleep(3)
        reverse()
        print 'Reverse'
        time.sleep(3)
        spinRight()
        print 'Spin Right'
        time.sleep(3)
        spinLeft()
        print 'Spin Left'
        time.sleep(3)
        stop()
        print 'Stop'
        time.sleep(3)

except KeyboardInterrupt:
    print

finally:
    gpio.cleanup()
    
