import sys, time
import robohat

robohat.init()



try:
    lastL = robohat.irLeft()
    lastR = robohat.irRight()
    lastLineL = robohat.irLeftLine()
    lastLineR = robohat.irRightLine()
    print 'Left, Right, LeftLine, RightLine:', lastL, lastR, lastLineL, lastLineR
    print
    while True:
        newL = robohat.irLeft()
        newR = robohat.irRight()
        newLineL = robohat.irLeftLine()
        newLineR = robohat.irRightLine()
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
    robohat.cleanup()
