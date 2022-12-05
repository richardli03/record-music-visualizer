"""
turn the DC motor on and spin the servo for a few seconds
"""

from timeit import default_timer as timer
from send_serial import *
import pandas as pd

# For testing
stepper_multiplier = 0.7

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
        move_amount_steps = move_amount * 1.8 * stepper_multiplier

        if self._name == "bass":
            # move calibration
            stepper("a", int(move_amount_steps))
            return
            
        if self._name == "mid":
            # move calibration
            
            stepper("b", int(move_amount_steps))
            return
            
        if self._name == "treb":
            # move calibration
            
            stepper("c", int(move_amount_steps))
            pass
    
    def __repr__(self) -> str:
        return f"Stepper motor {self._name}"


def compute_DC_speed(song_length) -> float:
    """
    Given some song length (in seconds), compute
    the speed of the DC motor necessary to make that happen
    """
    # line of best fit 
    if song_length > 100:
        motor_speed = 150 - 0.902*song_length + 0.00204*(song_length^2)
    else:
        motor_speed = 1328 - 27.5*song_length + 0.152*(song_length^2)
        

    return motor_speed

def theta_to_seconds(theta, song_length):
    """
    Given the length of the song and an angle, compute what 
    time should be equivalent to this angle.

    Args:
        theta (int): the angle in question, in degrees
        song_length (int): the length of the song
    
    Returns: 
        seconds: the number of seconds that should've passed to this theta
    """
    
    sec_per_d = song_length/360
    return theta * sec_per_d
    
def main():
    # First thing to do is rotate the thing at the correct speed:
    song_length = 177 # s || pretend it's a 2 minute song
    
    # initialize stepper motors
    bass = Stepper("bass")
    mid = Stepper("mid")
    treble = Stepper("treb")

    song_data = pd.read_csv("datasets/herestous.csv").transpose()
    
    # Catch errors
    if song_data.empty:
        print("No song data found!")
        return 
    
    num_samples = list(song_data.columns)

    # Convert the theta column to how many seconds it should be before the thing is where it is.
    seconds_for_movement = pd.DataFrame([theta_to_seconds(song_data[sample][0], song_length) for sample in num_samples]).transpose()
    
    # Get rid of theta data and add in seconds data
    song_data.drop(["theta"], inplace= True, axis = 0)
    song_data = pd.concat([seconds_for_movement, song_data])
    
    
    # start spinning the disk)
    dc_speed(compute_DC_speed(song_length))

    t_start = timer() # time since Jan 1, 1970 for timer purposes
    b_old = 0
    m_old = 0
    t_old = 0
    for sample in num_samples:
        # Split the new row of values into their components
        
        next_sample = song_data[sample]
        vals = next_sample.to_list()
        seconds = vals[0]
        
        # i think this should prevent the steppers from moving faster than we want them to. 
        # may need to calibrate some stuff
        while timer() - seconds < t_start:
            pass
        
        # Get bass, mid, treble frequences
        bass.move(vals[1]-b_old)
        mid.move(vals[2]-m_old)
        treble.move(vals[3]-t_old)    
        
        b_old = vals[1]
        m_old = vals[2]
        t_old = vals[3]  
        
        # Compute the stepper motor movement to correspond with an int


if __name__ == "__main__":
    main()