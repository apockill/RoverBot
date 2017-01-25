# initio Servo Test using simple PWM
# Do not expect this to be reliable or stable
# Moves the servo left, centre, right and repeats
# Press Ctrl-C to stop
#
# Please use servoTest.py for correct operation
#
# Run using: sudo python servoTest.py


import time, RPi.GPIO as gpio

servo = 22

gpio.setmode(gpio.BOARD)
gpio.setup(servo, gpio.OUT)


p = gpio.PWM(servo, 200)   # frequency is 500Hz, so each pulse is 5ms wide
# servos will be fully left at 0.5ms, centred at 1.5ms and fully right at 2.5ms

left = 50/5
right = 250/5
centre = 150/5

p.start(centre) # start it at 50% - should be centre of servo
#p.ChangeDutyCycle(100)

print "Testing servo on pin", servo
print

# main loop
try:
    while True:
        p.ChangeDutyCycle(centre)
        print 'Centre'
        time.sleep(2)
        p.ChangeDutyCycle(left)
        print 'Left'
        time.sleep(2)
        p.ChangeDutyCycle(centre)
        print 'Centre'
        time.sleep(2)
        p.ChangeDutyCycle(right)
        print 'Right'
        time.sleep(2)

except KeyboardInterrupt:
    print

finally:
    gpio.cleanup()
    
