"""
Functions for sending motor drive commands to the Arduino over a
serial connection.
"""
import time
import serial # pySerial usually comes preinstalled on raspbian

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
time.sleep(1.5) # allow time to connect before sending commands

def dc_speed(speed):
    """
    Control the speed of the DC motor.

    Args:
        speed (int): the motor speed on scale of 0-255
    """
    command = f"(dr{speed})"
    arduino.write(bytes(command, 'utf-8'))


def dc_off():
    """
    Control the state (on/off) of the DC motor.
    """
    arduino.write(bytes("(ds)", 'utf-8'))


def stepper(stepper, steps):
    """
    Control any of the stepper motors and how much it will rotate by.

    Args:
        stepper (str): which stepper is to be controlled (a, b, c)
        turn_amount (int): steps of rotation (1.8 degrees per step)
    """

    command = f"(s{stepper}{steps})"
    arduino.write(bytes(command, 'utf-8'))

if __name__ == "__main__": 
    print(":)")

