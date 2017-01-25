# initio Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# Also demonstrates writing to the LEDs
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTest.py


import robohat, time

speed = 80
print "Tests the motors at speed = 80%"
print "Forward, Reverse, Spin Right, Spin Left, Stop, then repeat"
print "Press Ctrl-C to stop"
print

robohat.init()

# main loop
try:
    while True:
        robohat.forward(speed)
        print 'Forward'
        time.sleep(3)
        robohat.reverse(speed)
        print 'Reverse'
        time.sleep(3)
        robohat.spinRight(speed)
        print 'Spin Right'
        time.sleep(3)
        robohat.spinLeft(speed)
        print 'Spin Left'
        time.sleep(3)
        robohat.stop()
        print 'Stop'
        time.sleep(3)

except KeyboardInterrupt:
    print

finally:
    robohat.cleanup()
    
