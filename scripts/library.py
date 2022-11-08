import os
import sys
repository_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.append(repository_root)

import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as f
import pandas as pd
import librosa as l
import librosa.display as disp
import pdb

# control visibility of visuals
DISPLAY = False
FREQ = True

# initialize global variables
INPUT_FILE, song, sr, song_length, sample_length, num_samples = None

def input_file(audio):
    """
    Sets audio file for all the following functions. Loads song.

    Args:
        audio (string): file path to .wav audio file to be used for the rest of
            the functions
    """
    INPUT_FILE = audio
    
    song, sr = l.load(INPUT_FILE, mono = True)

    song_length = len(song)
    sample_length = 100 # length of one sample in ms
    num_samples = song_length // sample_length # the number of samples we have

def display_visuals(choice):
    """
    Changes state of DISPLAY. By default it's false.

    Args:
        choice (bool): True means it will display, False means it won't
    """
    DISPLAY = choice

def make_freq_spread(x, Fs, plot):
    """
    Make a frequency domain plot with labels
    
    Args:
        x (array): song data
        Fs (int): sampling rate
        plot (bool): add plot data
    """

    song_length = len(x)

    if song_length%2 != 0:
        song_length -= 1
        x = x[:song_length]

    # linspace represents the frequency spread
    freq_space =np.linspace(-Fs/2, Fs/2-Fs/song_length,song_length), 1/song_length*f.fftshift(abs(f.fft(x))) 
    if plot:
      plt.plot(freq_space[0], (1/song_length)*f.fftshift(abs(f.fft(x)))) # frequency vs volume
    
    song_data = (1/song_length)*f.fftshift(abs(f.fft(x))) # shit data to center about zero
    return song_data, freq_space

def plot_song(x):
    plt.plot(x)
    plt.show()
    
def data_splitter(freq_data):
  """
  Split and process all of the frequency data into 3 different data sets: bass, mid, and treble

  Args:
      freq_data (pandas Dataframe): a dataframe with all of the frequency data over the course of a song
  """
  
  # takes lower half of symmetric fft data
  halved_data = freq_data[len(freq_data)//2:]

  length = len(halved_data)

  # compute logarithmic cutoffs for frequency ranges
  max_log = np.log10(halved_data.iloc[length - 1, 0])
  bass_cutoff = int(10**(max_log*(1/3)) + 20) # can be tuned.
  mid_cutoff = int(20 + 10**(max_log*(2/3))) # can be tuned.

  # split data into treble, mid, bass:
  bass_data = halved_data[:bass_cutoff]
  mid_data = halved_data[bass_cutoff:mid_cutoff]
  treble_data = halved_data[mid_cutoff:]
  
  return bass_data, mid_data, treble_data

def weighted_avg(freqs):
  """
  Take the weighted average of a subset frequency

  Args:
      freqs (pandas Dataframe): one "bucket" frequency split with volume by
        frequencies over time
  """

  weights = []
  val_weights = []
  
  for val in freqs:
    if val < -70: # filter out quiet/ambient noise
      weight = 0.01
    if val > -50: # weight actual signals so they show up
      weight = 150
    else:
      weight = 1
    
    val_weights.append(val*weight)
    weights.append(weight)
    
  # if every signal was < -70 dB
  if len(set(weights)) == 1:
    return -100
  
  return sum(val_weights)/sum(weights)
        
def compute_volumes(subset_freq):
  """
  Compute the volume/time of a frequency spectrum over time

  Args:
      subset_freq (pandas Dataframe): a dataframe with all the frequency data of a certain spectrum over the course of a song
  """
  
  average = []

  for column in subset_freq:
    mean_of_column = weighted_avg(subset_freq[column])
    average.append(mean_of_column)
    
  return average

if __name__ == "main" :
    print("a funky fresh disco diva")