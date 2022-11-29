"""
turn the DC motor on and spin the servo for a few seconds
"""

import time
from send_serial import *
import pandas as pd

class Stepper:
    def __init__(self, name):
        self._name = name
        pass
    
    def move(self, value):
        """
        As a reminder to me, the "value" is going to be a 
        rigid distance away from its "center line"

        Args:
            value (_type_): _description_
        """
        move_amount = 1139*value + -17.9
        
        if self._name == "bass":
            
            # move calibration
            stepper("a", move_amount)
            return
            
        if self._name == "mid":
            # move calibration
            
            stepper("b", move_amount)
            return
            
        if self._name == "treb":
            # move calibration
            
            stepper("c", move_amount)
            pass
    
    def __repr__(self) -> str:
        return f"Stepper motor {self._name}"



def compute_DC_speed(song_length) -> float:
    """
    Given some song length (in seconds), compute
    the speed of the DC motor necessary to make that happen
    """
    # line of best fit 
    motor_speed = 182 + -1.19*song_length + 0.0026*(song_length^2)
    return motor_speed
    
    
def main():
    # First thing to do is rotate the thing at the correct speed:
    dc_speed(200) #compute_DC_speed
    
    
    bass = Stepper("bass")
    mid = Stepper("mid")
    treble = Stepper("treb")

    song_data = pd.read_csv("datasets/pos_data.csv").transpose()
    print(song_data)
    
    #send_serial.dc_speed(compute_DC_speed(song_length))


    if not song_data.empty:
        next_sample = song_data[0]

    num_samples = list(song_data.columns)

    for sample in num_samples:
        # Split the new row of values into their components
        
        next_sample = song_data[sample]
        vals = next_sample.to_list()

        # TODO: We do have to connect time with this angle
        theta = vals[0]

        # Get bass, mid, treble frequences
        bass.move(vals[1])
        mid.move(vals[2])
        treble.move(vals[3])      
        
        print(bass, mid, treble)
        
        # Compute the stepper motor movement to correspond with an int


if __name__ == "__main__":
    main()