

def clamp(val, low, max):
    # Clamp a value between a min and max

    if val < low:
        return low

    elif val > max:
        return max

    return val


def sign(val):
    # Return the sign of a value. 0 is positive
    if val < 0:
        return -1
    return 1


class FpsTimer:
    """
    This module helps keep scripts at a certain FPS. The Interpreter script uses this, as does the VideoThread.
    This will effectively decide whether or not to wait, and how much to wait, and time how long a script is taking
    inside of a loop.

    Usage example:

            fpsTimer = FpsTimer(fps=24)

            while True:
                fpsTimer.wait()
                if not fpsTimer.ready(): continue

                ### Script goes here ###
    """

    def __init__(self, fps):

        self.fps       = fps
        self.stepDelay = (1.0 / float(fps))
        self.lastTime  = float(1)  # The first time is 1, so the script will always run immediately
        self.isReady   = False
        self.mode      = 1

        self.currentFPS = 0

    def wait(self):
        elapsedTime = time() - self.lastTime


        # Check if the current FPS is less than the goal. If so, run immediately
        if not elapsedTime == 0:
            fps = 1.0 / elapsedTime
            if fps < self.fps:
                self.currentFPS = fps
                self.isReady = True
                return

        # Since the current FPS is higher than desired, wait the appropriate amount of time
        waitTime = self.stepDelay - elapsedTime
        if waitTime > .01:
            sleep(waitTime)
            self.currentFPS = 1.0 / (time() - self.lastTime)

        # Calculate FPS again
        self.isReady = True
        return

    def ready(self):

        if self.isReady:
            self.lastTime = time()
            self.isReady = False
            return True
        else:
            return False
