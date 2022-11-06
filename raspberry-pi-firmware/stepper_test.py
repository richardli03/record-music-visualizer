import RPI.GPIO as GPIO

# import motor library
from RpiMotorLib import RpiMotorLib

# define GPIO pins
direction = 14
step = 15

# don't want to be fancy for this test so ignore Microstepping pins
MSX = (-1,-1,-1)

# create instance of motor class
mymotortest = RpiMotorLib.A4988Nema(direction, step, MSX, "DRV8825")

# 180 degree clockwise turn for 50 steps, a step delay of.01, verbose output
# off, and a 50 ms initial delay
mymotortest.motor_go(False, "Full", 50, .01, False, .05)