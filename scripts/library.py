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
# FROM_CSV = True 

FREQ_SPLIT_VECTOR = [0.41, 0.58, 0.8] # split, split, ceiling

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
    global sample_length; sample_length = 30000 # milliseconds
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
  bass_cutoff = int(10**(max_log*(FREQ_SPLIT_VECTOR[0]))) # can be tuned
  mid_cutoff = int(10**(max_log*(FREQ_SPLIT_VECTOR[1]))) # can be tuned
  treb_cutoff = int(10**(max_log*(FREQ_SPLIT_VECTOR[2]))) # ceiling for frequencies
  
  # split data
  bass_data = halved_data[:bass_cutoff]
  mid_data = halved_data[bass_cutoff:mid_cutoff]
  treble_data = halved_data[mid_cutoff:treb_cutoff]
  
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
    if val < -75: # filter out quiet/ambient noise
      weight = 0.01
    elif val > -50: # weight actual signals so they show 
      weight = 3
    else:
      weight = 1
    
    val_weights.append(val*weight)
    weights.append(weight)
    
  # if every signal was < -75 dB
  if len(set(weights)) == 1 and weights[0] == 0.01:
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

def create_freq_data(FROM_CSV):
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
    samples = np.linspace(0, song_length, num_samples, dtype = "int") # create a linspace for time (by sample)

    all_freq_data = pd.DataFrame(columns = samples)

    for i, sample in enumerate(samples[:-1]):
      freq_data, freq_space = make_freq_spread(song[samples[i]:samples[i+1]], sr, False)
      all_freq_data[sample] = pd.Series(l.amplitude_to_db(freq_data))

    all_freq_data.to_csv("all_freq_data.csv")

  return all_freq_data  

def process(input, FROM_CSV):
  """
  Tie together all the functions so you can start with an audio input
  and get out the data for volume over time for bass, mid, and treble.

  Args:
    input (string): file path to .wav audio file to be used for the rest of
      the functions
    FROM_CSV (bool): True means read from the csv called all_freq_data, False
      means make the freq. spread and create the csv. This improves runtime.
  """

  input_file(input)
  all_freq_data = create_freq_data(FROM_CSV)
  bass_data, mid_data, treble_data = data_splitter(all_freq_data)
  bass_data.to_csv('bass_data.csv')
  mid_data.to_csv('mid_data.csv')
  treble_data.to_csv('treb_data.csv')
    
  b_o_t = compute_volumes(bass_data)
  m_o_t = compute_volumes(mid_data)
  t_o_t = compute_volumes(treble_data)

  return b_o_t, m_o_t, t_o_t

def plot_volume(bot, mot, tot):
  """
  Take bass mid or treble volumes over time and plot them on a graph (normal).

  Args:
    bot (array): average bass volume over time
    mot (array): average mid volume over time
    tot (array): average treble volume over time
  """

  plt.plot(bot)
  plt.plot(mot)
  plt.plot(tot)
    
  plt.legend(["bass","mid","treble"])
  plt.show()

def scale_data(pos_data):
  """
  Scales data so it goes from -1 to 1.

  Args:
    pos_data (pandas dataframe): has four columns, the first for radians,
      and then one for the radius of each bucket. the indices are times.
  """

  largest_value = pos_data.abs().max().max()
  scale_factor = 1/largest_value

  return pos_data * scale_factor

def create_osciallations(pos_data):
  """
  Takes basic volume over time data for each bucket and adds in oscillations
  to make it more visually representative.

  Args:
    pos_data (pandas dataframe): has radians in the first column and radius
      variation data for each bucket in the following columns.
  """

  # going to create twice as many data points as original so we can create
  # waves using the extra datapoints
  new_radians = np.linspace(0, 2*np.pi, len(pos_data.iloc[:,0]) * 2)
  final_data = pd.DataFrame(index=new_radians)
  baseline_amplitude = 0.2 # amplitude of band of 0 data. also the threshold for 0 data.
  osc_sign = -1 # flips with every data point to create oscillations

  for c in pos_data:
    column = pos_data[c]
    r = []
    
    for i in range(len(column)-1):
      current = column.iloc[i]
      next = column.iloc[i+1]

      r.append(current) # add current radius datapoint to new radius list

      # add in the intermediate point between two current datapoints (with the
      # correct sign)
      if current < baseline_amplitude and next < baseline_amplitude:
        r.append(baseline_amplitude * osc_sign)
        osc_sign = -osc_sign
      else:
        sign = current/abs(current) * -1
        r.append(baseline_amplitude * sign)

    # add the last two values (that we can't index through the loop)
    r.append(current)
    r.append(r[0])

    final_data.insert(len(final_data.columns), column.name, r)

  return final_data

def plot_polar(pos_data):
  """
  Takes position data that's sent to the servos and plots it.

  Args:
    pos_data (pandas dataframe): has radians in the first column and radius
      variations for each bucket in the next columns.
  """

  radii = [1, 3, 5] # baseline radii (no var) for each bucket

  radians = pos_data.index

  for i in range(3):
    column = pos_data.iloc[:, i]
    baseline_radius = radii[i]

    r = column + baseline_radius

    plt.polar(radians, r)

  plt.grid(False)
  plt.yticks([])
  plt.xticks([])

  plt.show()

def create_record_visual_data(bot, mot, tot, to_draw):
  """"
  Visualize the different ranges' volume over time the way our mechanism
  would draw it.

  Args:
    bot (array): average bass volume over time
    mot (array): average mid volume over time
    tot (array): average treble volume over time
    to_draw (bool): controls whether to plot it or not
  """

  data = [bot, mot, tot]
  avgs = [np.average(bot), np.average(mot), np.average(tot)]

  radius_labels = ['r_bass', 'r_mid', 'r_treb']
  radians = np.linspace(0, 2*np.pi, num_samples, True)
  pos_data = pd.DataFrame(index=radians)

  for i in range(3):

    # find variation of each datapoint from average and normalize it
    # divides by the range of values in that data set
    if np.ptp(data[i]) == 0:
      radius_var = np.zeros(num_samples)
    else:
      radius_var = (data[i] - avgs[i])/np.ptp(data[i])
      radius_var = radius_var[:num_samples]
      # note, chopping radius_var might cause problems later
    
    pos_data.insert(i, radius_labels[i], radius_var)

  # remove first row before scaling it because that always has a weirdly high value
  sliced_pos_data = pos_data.iloc[1:]
  scaled_data = scale_data(sliced_pos_data)

  final_data = create_osciallations(scaled_data)

  if to_draw:
    plot_polar(final_data)

  return final_data

if __name__ == "main" :
    print("a funky fresh disco diva")
