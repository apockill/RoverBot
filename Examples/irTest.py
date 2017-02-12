import time

from HardwareLibs import RoboHat

RoboHat.init()



try:
    lastL = RoboHat.irLeft()
    lastR = RoboHat.irRight()
    lastLineL = RoboHat.irLeftLine()
    lastLineR = RoboHat.irRightLine()
    print 'Left, Right, LeftLine, RightLine:', lastL, lastR, lastLineL, lastLineR
    print
    while True:
        newL = RoboHat.irLeft()
        newR = RoboHat.irRight()
        newLineL = RoboHat.irLeftLine()
        newLineR = RoboHat.irRightLine()
        if (newL != lastL) or (newR != lastR) or (newLineL != lastLineL) or (newLineR != lastLineR):
            print 'Left, Right, LeftLine, RightLine:', newL, newR, newLineL, newLineR
            print
            lastL = newL
            lastR = newR
            lastLineL = newLineL
            lastLineR = newLineR
        time.sleep(0.1)
                          
except KeyboardInterrupt:
    print

finally:
    RoboHat.cleanup()
