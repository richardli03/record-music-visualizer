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

# keeps track of whether to read all_freq_data from a csv or make it again
# (makes runtime a lot shorter)
FROM_CSV = True 

def input_file(audio):
    """
    Sets audio file for all the following functions. Loads song.

    Args:
        audio (string): file path to .wav audio file to be used for the rest of
            the functions
    """
    global INPUT_FILE; INPUT_FILE = audio
    global song; global sr
    song, sr = l.load(INPUT_FILE, mono = True)

    global song_length; song_length = len(song)
    global sample_length; sample_length = 100 # milliseconds
    global num_samples; num_samples = song_length // sample_length

def make_freq_spread(x, Fs, plot):
    """
    Make a frequency domain plot with labels
    
    Args:
        x (array): a sample in the song data (a small time period)
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
  
  freq_data = freq_data.fillna(value = -100) #NaNs become -100
  halved_data = freq_data[len(freq_data)//2:] #takes last half of data

  length = len(halved_data)

  # compute logarithmic cutoffs
  # last_row = halved_data.iloc[length - 1].index
  last_row = length - 1
  max_log = np.log10(last_row)
  bass_cutoff = int(10**(max_log*(1/3)) + 20) # can be tuned
  mid_cutoff = int(20 + 10**(max_log*(2/3))) # can be tuned

  # split data
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

def create_freq_data():
  """
  Put all the data from the song into a data frame with time (which is in
  samples) along the columns and frequencies as the rows.

  If a CSV of it exists, get it from there to reduce runtime. Otherwise create
  it by making a frequency spread, etc.

  Note, you need to make a new csv every time you use a new sample.

  Args:
    None
  """
  if FROM_CSV:
    all_freq_data = pd.read_csv('all_freq_data.csv')
  else:
    samples = np.linspace(0, song_length, int(song_length//num_samples), dtype = "int") # create a linspace for time (by sample)

    all_freq_data = pd.DataFrame(columns = samples)

    for i, sample in enumerate(samples[:-1]):
      freq_data, freq_space = make_freq_spread(song[samples[i]:samples[i+1]], sr, False)
      all_freq_data[sample] = pd.Series(l.amplitude_to_db(freq_data))

    create_csv(all_freq_data)  

  return all_freq_data

def create_csv(data):
  """
  Save all_freq_data from create_freq_data as a csv.

  Args:
    None
  """
  data.to_csv("all_freq_data.csv")


def plot_volumes(input):
  """
  Tie together all the functions so you can start with an audio input
  and get out the plots of volume over time for bass, mid, and treble.

  Args:
    input (string): file path to .wav audio file to be used for the rest of
      the functions
  """

  input_file(input)
  all_freq_data = create_freq_data()
  bass_data, mid_data, treble_data = data_splitter(all_freq_data)
    
  b_o_t = compute_volumes(bass_data)
  m_o_t = compute_volumes(mid_data)
  t_o_t = compute_volumes(treble_data)
    
    
  plt.plot(b_o_t)
  plt.plot(m_o_t)
  plt.plot(t_o_t)
    
  plt.legend(["bass","mid","treble"])
  plt.show()

  return b_o_t, m_o_t, t_o_t

def draw_record_visual(bot, mot, tot):
  """"
  Visualize the different ranges' volume over time the way our mechanism
  would draw it.

  Args:
    bot (array): average bass volume over time
    mot (array): average mid volume over time
    tot (array): average treble volume over time
  """

  data = [bot, mot, tot]
  radii = [1, 3, 5] # baseline radii (no var) for each bucket
  avgs = [np.average(bot), np.average(mot), np.average(tot)]

  # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

  for i in range(3):
    # find variation of each datapoint from average and normalize it
    radius_var = (data[i] - avgs[i])/np.ptp(data[i])
    r = radii[i] + radius_var

    theta = np.linspace(0, 2*np.pi, len(data[i]), True)

    plt.polar(theta, r)

  plt.grid(False)
  plt.yticks([])
  plt.xticks([])

  plt.show()

if __name__ == "main" :
    print("a funky fresh disco diva")