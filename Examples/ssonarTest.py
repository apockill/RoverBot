import time
import RoboHat

RoboHat.init()

try:
    while True:
        dist = RoboHat.getDistance()
        print "Distance: ", int(dist)
        time.sleep(1)

except KeyboardInterrupt:
    print
    pass

finally:
    RoboHat.cleanup()
