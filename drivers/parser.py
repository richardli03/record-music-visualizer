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
    
    def move(self, value):
        if self.name == "bass":
            # move calibration
            pass
            
        if self.name == "mid":
            # move calibration
            pass
            
        if self.name == "treb":
            # move calibration
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

def main():
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