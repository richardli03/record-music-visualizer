"""
Functions for sending motor drive commands to the Arduino over a
serial connection.
"""

import serial

def dc_control():
    """
    Control the state (on/off) and speed (0-255) of the DC motor.
    """
    pass

def stepper_control(stepper, turn_amount):
    """
    Control any of the stepper motors and how much it will rotate by.

    Note: turn_amount is in degrees at time of programming but might
    change to # steps
    """
    pass