#!/usr/bin/python
#
# Python Module to externalise all Initio/RoboHAT specific hardware
#
# Created by Gareth Davies, Feb 2016
# Copyright 4tronix
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
# ======================================================================


# ======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors off, etc
# cleanup(). Sets all motors off and sets GPIO to standard values
# version(). Returns 2. Invalid until after init() has been called
# ======================================================================


# ======================================================================
# Motor Functions
#
# stop(): Stops both motors
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# turnreverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# ======================================================================


# ======================================================================
# IR Sensor Functions
#
# irLeft(): Returns state of Left IR Obstacle sensor
# irRight(): Returns state of Right IR Obstacle sensor
# irAll(): Returns true if either of the Obstacle sensors are triggered
# irLeftLine(): Returns state of Left IR Line sensor
# irRightLine(): Returns state of Right IR Line sensor
# ======================================================================


# ======================================================================
# UltraSonic Functions
#
# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
# ======================================================================

# ======================================================================
# Servo Functions
# 
# startServos(). Initialises the servo background process
# stop Servos(). terminates the servo background process
# setServo(Servo, Degrees). Sets the servo to position in degrees -90 to +90
# ======================================================================


# Import all necessary libraries
import RPi.GPIO as GPIO, sys, threading, time, os, subprocess

# Pins 35, 36 Left Motor
# Pins 32, 33 Right Motor
L1_Pin = 36
L2_Pin = 35
R1_Pin = 33
R2_Pin = 32

# Define obstacle sensors and line sensors
# These can be on any input pins, but this library assumes the following layout
# which matches the build instructions
irFL = 7
irFR = 11
lineLeft = 29
lineRight = 13

# Define Sonar Pin (Uses same pin for both Ping and Echo)
sonar = 38

ServosActive = False


# ======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors and LEDs Off, etc
def init():
    global L1_PWM, L2_PWM, R1_PWM, R2_PWM

    GPIO.setwarnings(False)

    # use physical pin numbering
    GPIO.setmode(GPIO.BOARD)
    # print GPIO.RPI_REVISION

    # set up digital line detectors as inputs
    GPIO.setup(lineRight, GPIO.IN)  # Right line sensor
    GPIO.setup(lineLeft, GPIO.IN)  # Left line sensor

    # Set up IR obstacle sensors as inputs
    GPIO.setup(irFL, GPIO.IN)  # Left obstacle sensor
    GPIO.setup(irFR, GPIO.IN)  # Right obstacle sensor

    # p L1
    # q L2
    # a R1
    # b #R2

    # use pwm on inputs so motors don't go too fast
    # GPIO.setup(L1_Pin, GPIO.OUT)
    # L1_PWM = GPIO.PWM(L1_Pin, 20)
    # L1_PWM.start(0)
    #
    # GPIO.setup(L2_Pin, GPIO.OUT)
    # L2_PWM = GPIO.PWM(L2_Pin, 20)
    # L2_PWM.start(0)

    GPIO.setup(R1_Pin, GPIO.OUT)
    R1_PWM = GPIO.PWM(R1_Pin, 20)
    R1_PWM.start(0)

    GPIO.setup(R2_Pin, GPIO.OUT)
    R2_PWM = GPIO.PWM(R2_Pin, 20)
    R2_PWM.start(0)

    startServos()


# cleanup(). Sets all motors off and sets GPIO to standard values
def cleanup():
    stop()
    stopServos()
    GPIO.cleanup()


# version(). Returns 2. Invalid until after init() has been called
def version():
    return 2  # (version 1 is Pirocon, version 2 is RoboHAT)


# End of General Functions
# ======================================================================


# ======================================================================
# Motor Functions
#
# stop(): Stops both motors
def stop():
    L1_PWM.ChangeDutyCycle(0)
    L2_PWM.ChangeDutyCycle(0)
    R1_PWM.ChangeDutyCycle(0)
    R2_PWM.ChangeDutyCycle(0)


# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
def forward(speed):
    L1_PWM.ChangeDutyCycle(speed)
    L2_PWM.ChangeDutyCycle(0)
    R1_PWM.ChangeDutyCycle(speed)
    R2_PWM.ChangeDutyCycle(0)
    L1_PWM.ChangeFrequency(speed + 5)
    R1_PWM.ChangeFrequency(speed + 5)


# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
def reverse(speed):
    L1_PWM.ChangeDutyCycle(0)
    L2_PWM.ChangeDutyCycle(speed)
    R1_PWM.ChangeDutyCycle(0)
    R2_PWM.ChangeDutyCycle(speed)
    L2_PWM.ChangeFrequency(speed + 5)
    R2_PWM.ChangeFrequency(speed + 5)


# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinLeft(speed):
    L1_PWM.ChangeDutyCycle(0)
    L2_PWM.ChangeDutyCycle(speed)
    R1_PWM.ChangeDutyCycle(speed)
    R2_PWM.ChangeDutyCycle(0)
    L2_PWM.ChangeFrequency(speed + 5)
    R1_PWM.ChangeFrequency(speed + 5)


# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinRight(speed):
    L1_PWM.ChangeDutyCycle(speed)
    L2_PWM.ChangeDutyCycle(0)
    R1_PWM.ChangeDutyCycle(0)
    R2_PWM.ChangeDutyCycle(speed)
    L1_PWM.ChangeFrequency(speed + 5)
    R2_PWM.ChangeFrequency(speed + 5)


# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnForward(leftSpeed, rightSpeed):
    L1_PWM.ChangeDutyCycle(leftSpeed)
    L2_PWM.ChangeDutyCycle(0)
    R1_PWM.ChangeDutyCycle(rightSpeed)
    R2_PWM.ChangeDutyCycle(0)
    L1_PWM.ChangeFrequency(leftSpeed + 5)
    R1_PWM.ChangeFrequency(rightSpeed + 5)


# turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnReverse(leftSpeed, rightSpeed):
    L1_PWM.ChangeDutyCycle(0)
    L2_PWM.ChangeDutyCycle(leftSpeed)
    R1_PWM.ChangeDutyCycle(0)
    R2_PWM.ChangeDutyCycle(rightSpeed)
    L2_PWM.ChangeFrequency(leftSpeed + 5)
    R2_PWM.ChangeFrequency(rightSpeed + 5)


# End of Motor Functions
# ======================================================================


# ======================================================================
# IR Sensor Functions
#
# irLeft(): Returns state of Left IR Obstacle sensor
def irLeft():
    if GPIO.input(irFL) == 0:
        return True
    else:
        return False


# irRight(): Returns state of Right IR Obstacle sensor
def irRight():
    if GPIO.input(irFR) == 0:
        return True
    else:
        return False


# irAll(): Returns true if any of the Obstacle sensors are triggered
def irAll():
    if GPIO.input(irFL) == 0 or GPIO.input(irFR) == 0:
        return True
    else:
        return False


# irLeftLine(): Returns state of Left IR Line sensor
def irLeftLine():
    if GPIO.input(lineLeft) == 0:
        return True
    else:
        return False


# irRightLine(): Returns state of Right IR Line sensor
def irRightLine():
    if GPIO.input(lineRight) == 0:
        return True
    else:
        return False


# End of IR Sensor Functions
# ======================================================================


# ======================================================================
# UltraSonic Functions
#
# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
def getDistance():
    GPIO.setup(sonar, GPIO.OUT)
    # Send 10us pulse to trigger
    GPIO.output(sonar, True)
    time.sleep(0.00001)
    GPIO.output(sonar, False)

    start = time.time()
    count = time.time()
    GPIO.setup(sonar, GPIO.IN)
    while GPIO.input(sonar) == 0 and time.time() - count < 0.1:
        start = time.time()

    count = time.time()
    stop = count
    while GPIO.input(sonar) == 1 and time.time() - count < 0.1:
        stop = time.time()

    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance


# End of UltraSonic Functions
# ======================================================================

# ======================================================================
# Servo Functions
# Pirocon/Microcon/RoboHAT use ServoD to control servos


def setServo(Servo, Degrees):
    global ServosActive
    # print "ServosActive:", ServosActive
    # print "Setting servo"
    if ServosActive == False:
        startServos()
    pinServod(Servo, Degrees)  # for now, simply pass on the input values


def stopServos():
    stopServod()


def startServos():
    # print "Starting servod as CPU =", CPU
    startServod()


def startServod():
    global ServosActive
    # print "Starting servod. ServosActive:", ServosActive
    SCRIPTPATH = os.path.split(os.path.realpath(__file__))[0]
    os.system("sudo pkill -f servod")
    initString = "sudo " + SCRIPTPATH + '/servod --pcm --idle-timeout=20000 --p1pins="18,22" > /dev/null'
    os.system(initString)
    ServosActive = True


def pinServod(pin, degrees):
    # print pin, degrees
    pinString = "echo " + str(pin) + "=" + str(50 + ((90 - degrees) * 200 / 180)) + " > /dev/servoblaster"
    # print pinString
    os.system(pinString)


def stopServod():
    global ServosActive
    os.system("sudo pkill -f servod")
    ServosActive = False
