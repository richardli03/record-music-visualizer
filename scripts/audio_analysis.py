# import packages to be able to run from correct place
import os
import sys
repository_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.append(repository_root)

# import packages to analyze and visualize data
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as f
import pandas as pd
import librosa as l
import librosa.display as disp

import pdb
# specify which audio file we're using
# INPUT_FILE = "../assets/mids.wav"
INPUT_FILE = "../assets/365.wav"

# booleans to specify whether to show visuals or not
DISPLAY = False
FREQ = True
 
 # librosa package that loads song into data points
 # sr is the sample rate, song is all the data points
song, sr = l.load(INPUT_FILE, mono = True)

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
        # np.append(x,(x[-1]))
        song_length -= 1
        x = x[:song_length]

    # makes a linspace for the frequency spread, take fft
    freq_space =np.linspace(-Fs/2, Fs/2-Fs/song_length,song_length), 1/song_length*f.fftshift(abs(f.fft(x))) 
    if plot:
      plt.plot(freq_space[0], (1/song_length)*f.fftshift(abs(f.fft(x)))) # plots frequency vs volume
    
    song_data = (1/song_length)*f.fftshift(abs(f.fft(x))) # center data about zero
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
  
  # Split the rows in half -- from 1780 to 0:889
  # freq_data = freq_data.fillna(value = -100)
  halved_data = freq_data[:len(freq_data)//2]
  halved_data.to_csv('halved_data.csv')

  length = len(halved_data)
  print(halved_data.iloc[length - 1, 0])

  # compute logarithmic cutoffs for frequency ranges
  max_log = np.log10(halved_data.iloc[length - 1, 0])
  print("max log", max_log)
  bass_cutoff = int(10**(max_log/3)) # defines a frequency as the border between bass and mid. to be tuned.
  print ("bass cutoff: ", bass_cutoff)
  mid_cutoff = int(10**(max_log*(2/3))) # defines border frequency between mid and high. to be tuned.
  print("mid cutoff: ", mid_cutoff)

  # split into treble, mid, bass:
  bass_data = halved_data[:30]
  mid_data = halved_data[30:100]
  treble_data = halved_data[100:]
  
  
  # Highest frequencies will be from 1300 - 1780
  # mid frequencies will be 400-550
  return bass_data, mid_data, treble_data

def weighted_avg(freqs):
  """
  Take the weighted average of a subset frequency

  Args:
      freqs (_type_): _description_
  """

  weights = []
  val_weights = []
  
  for val in freqs:
    if val < -70:
      weight = 0.01
    if val > -50:
      weight = 150
    else:
      weight = 1
    
    val_weights.append(val*weight)
    weights.append(weight)
    
  # if every signal was < -70 dB
  if len(set(weights)) == 1:
    return -100
  
  # pdb.set_trace()
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


  

def main():
  INPUT_FILE = "../assets/bass.wav"
  # INPUT_FILE = "assets/365.wav"
  DISPLAY = False
  FREQ = True
  
  song, sr = l.load(INPUT_FILE, mono = True)

  song_length = len(song)
  sample_length = 100 # length of one sample in ms
  num_samples = song_length // sample_length # the number of samples we have

  len_samples = np.linspace(0, len(song), len(song)//1764)

  if FREQ:
    samples = np.linspace(0, song_length, int(song_length//num_samples), dtype = "int") # create a linspace for time (by sample)

    # creates dataframe with samples as column headers and frequencies as row headers
    all_freq_data = pd.DataFrame(columns = samples)

    # iterates through samples (time steps)
    for i, sample in enumerate(samples[:-1]):

      # print(song[samples[i]:samples[i+1]])
      freq_data, freq_space = make_freq_spread(song[samples[i]:samples[i+1]], sr, True)

    # creating all_freq_data from csv to improve runtime (since right now we're
    # only looking at this one audio sample)
    all_freq_data = pd.read_csv('all_freq_data.csv')

      # plt.show()
      # plt.ylabel('Magnitude of signal')
      # plt.xlabel('Frequency (Hz)')
      # data_splitter(all_freq_data.fillna(value = -100))
      
    bass_data, mid_data, treble_data = data_splitter(all_freq_data)
    
    b_o_t = compute_volumes(bass_data)
    m_o_t = compute_volumes(mid_data)
    t_o_t = compute_volumes(treble_data)
    
    
    plt.plot(b_o_t)
    plt.plot(m_o_t)
    plt.plot(t_o_t)
    
    plt.legend(["bass","mid","treble"])
    plt.show()
    # bass_data.to_csv("bass_data.csv")
    # mid_data.to_csv("mid_data.csv")g
    # treble_data.to_csv("treble_data.csv")
      
    # print(compute_volumes(bass_data))
    
  if DISPLAY: 
    plt.show()
    plt.ylabel('Magnitude of signal')
    plt.xlabel('Frequency (Hz)')
    # all_freq_data.to_csv("all_freq_data.csv")
    
  
if __name__ == "__main__":
    main()