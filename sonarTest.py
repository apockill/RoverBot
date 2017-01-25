import time
import robohat

robohat.init()

try:
    while True:
        dist = robohat.getDistance()
        print "Distance: ", int(dist)
        time.sleep(.1)

except KeyboardInterrupt:
    print
    pass

finally:
    robohat.cleanup()
