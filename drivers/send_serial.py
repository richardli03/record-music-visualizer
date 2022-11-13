"""
Functions for sending motor drive commands to the Arduino over a
serial connection.
"""

import serial # pySerial usually comes preinstalled on raspbian

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

def dc_speed(speed):
    """
    Control the speed of the DC motor.

    Args:
        speed (int): the motor speed on scale of 0-255
    """
    command = f"dr{speed}"
    arduino.write(bytes(command, 'utf-8'))


def dc_off():
    """
    Control the state (on/off) of the DC motor.
    """
    arduino.write(bytes("ds", 'utf-8'))


def stepper_control(stepper, turn_amount):
    """
    Control any of the stepper motors and how much it will rotate by.

    Args:
        stepper (str): which stepper is to be controlled (a, b, c)
        turn_amount (int): degrees of rotation of stepper motor shaft (note:
        may change to number of steps)
    """
    command = f"s{stepper}{turn_amount}"
    arduino.write(bytes(command, 'utf-8'))