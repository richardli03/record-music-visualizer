"""
turn the DC motor on and spin the servo for a few seconds
"""

from timeit import default_timer as timer
from send_serial import *
import pandas as pd
import time


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

        # stepper motor calibration equation
        move_amount_steps = (625 * (-value) + -7.23)  #from inches to steps
        
        if move_amount_steps < 0:
                move_amount_steps *= 0.87
                
        
        if self._name == "bass":
            stepper("a", int(move_amount_steps))
            return
            
        if self._name == "mid":
            stepper("b", int(move_amount_steps))
            return
            
        if self._name == "treb":
            stepper("c", int(move_amount_steps))
            return
    
    def __repr__(self) -> str:
        return f"Stepper motor {self._name}"

def compute_DC_speed(song_length) -> float:
    """
    Given some song length (in seconds), compute
    the speed of the DC motor necessary to make that happen
    """
    # line of best fit 
    if song_length > 100:
        motor_speed = 152 - 0.902*song_length + 0.00204*(song_length**2)
    else:
        motor_speed = 1334 - 27.5*song_length + 0.152*(song_length**2) 

    print(f"Current DC speed is {motor_speed}")

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
    
    sec_per_r = song_length/6.283185307
    # sec_per_r = song_length/360
    return theta * sec_per_r


def create_song_data():
    song_data = pd.read_csv(INPUT_FILE).transpose()

    # Catch errors
    if song_data.empty:
        raise Exception("No song data found!")
        return 
    
    num_samples = list(song_data.columns)
    # Convert the theta column to how many seconds it should be before the thing is where it is.
    seconds_for_movement = pd.DataFrame([theta_to_seconds(song_data[sample][0], SONG_LENGTH) for sample in num_samples]).transpose()
    
    # Get rid of theta data and add in seconds data
    song_data.drop(["theta"], inplace= True, axis = 0)
    song_data = pd.concat([seconds_for_movement, song_data])
    return song_data, num_samples
    
    
def main():
    dc_off()
    
    # initialize stepper motors
    bass = Stepper("bass")
    mid = Stepper("mid")
    treble = Stepper("treb")

    # stepper calibration/initialization routine
    # sends each stepper to its initial position, assuming each starts
    # against its respective calibration block
    
    baseline_radii = [0.9, 2.8, 4.3] # inches
    blocks = [0, 1.5, 3.5] # length of the calibration blocks
    
    pos = [baseline_radii[i] - blocks [i] for i in range(3)]
    
    treble.move((1/0.9)* pos[2]) 
    time.sleep(1)
    mid.move((1/0.9)*pos[1])
    time.sleep(1)
    bass.move((1/0.9)*(pos[0]))
    time.sleep(1)
    
    song_data, num_samples = create_song_data()
    
    # debug = pd.DataFrame(columns = ["time", "bass","mid","treble"])
    print(song_data)
    
    current_pos = [0, 0, 0, 0]
    
    # Sleep before starting!
    print("ready to begin!")
    time.sleep(3)
    
    # start spinning the disk
    dc_speed(compute_DC_speed(SONG_LENGTH))  


    t_start = timer() # time since Jan 1, 1970 for timer purposes
  
    # current_time = 0
    
    for sample in num_samples:
        # Split the new row of values into their components
        next_sample = song_data[sample]
        vals = next_sample.to_list()
        seconds = vals[0]
        
        # # i think this should prevent the steppers from moving faster than we want them to. 
        # # may need to calibrate some stuff
        while timer() - (0.3 + seconds) < t_start:
            pass
        
        # Get bass, mid, treble positions, calculate change in position, and
        # move accordingly
        bass.move((vals[1]-current_pos[1])*STEPPER_SCALE)
        time.sleep(0.15)
        mid.move((vals[2]-current_pos[2])*STEPPER_SCALE)
        time.sleep(0.15)
        treble.move((vals[3]-current_pos[3])*STEPPER_SCALE)  
        
        # print(f"{seconds-current_time} seconds")
        # print(f"moving {(625 * (-(vals[2]-current_pos[2])) + -7.23)*STEPPER_SCALE} steps")
       
        # Add movement commands to a debug file 
        # debug.loc[len(debug)] = [seconds-current_time, vals[1]-current_pos[1],vals[2]-current_pos[2], vals[3]-current_pos[3]]

        # current_time = seconds
        current_pos = vals # stores current values 
    
    # debug.to_csv("debug4.csv")
    dc_off()

if __name__ == "__main__":
    SONG_LENGTH = 154 # s 
    INPUT_FILE = "datasets/love_story.csv"
    STEPPER_SCALE = 0.45
    main()