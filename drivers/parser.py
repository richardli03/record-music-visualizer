"""
turn the DC motor on and spin the servo for a few seconds
"""

import time
# import send_serial
import pandas as pd

class Stepper:

    def __init__(self, name):
        self.name = name
        
        pass
    
    def __repr__(self) -> str:
        return f"Stepper motor {self.name}"

def compute_DC_speed(song_length) -> float:
    """
    Given some song length (in seconds), compute
    the speed of the DC motor necessary to make that happen
    """

    #return motor_speed
    pass

# First thing to do is rotate the thing at the correct speed:
# send_serial.dc_speed(200) #compute_DC_speed

# bass = Stepper("bass")
# mid = Stepper("mid")
# treble = Stepper("treble")

song = True

song_data = pd.read_csv("datasets/test.csv").transpose()
print(song_data)
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
    bass = vals[1]
    mid = vals[2]
    treble = vals[3]
    # Compute the stepper motor movement to correspond with an int
       