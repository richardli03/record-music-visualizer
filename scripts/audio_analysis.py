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

INPUT_FILE = "../assets/bass.wav"
# INPUT_FILE = "assets/365.wav"
DISPLAY = False
FREQ = True
 
song, sr = l.load(INPUT_FILE, mono = True)

def make_freq_spread(x, Fs, plot):
    """
    Make a frequency domain plot with labels
    
    Args:
        x (array): song data
        Fs (int): sampling rate
        plot (bool): add plot data
    """

    if len(x)%2 != 0:
        # np.append(x,(x[-1]))
        x = x[:len(x-1)]

        
    freq_space =np.linspace(-Fs/2, Fs/2-Fs/len(x),len(x)), 1/len(x)*f.fftshift(abs(f.fft(x)))
    if plot:
      plt.plot(freq_space[0], (1/len(x))*f.fftshift(abs(f.fft(x))))
    
    song_data = (1/len(x))*f.fftshift(abs(f.fft(x)))
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

def main():
  print(len(song))
  
  
  # freq_data, freq_space = make_freq_plot(song[:3000],sr)
  # len_samples = np.linspace(0, len(song), len(song)//1764)

  if FREQ:
    samples = np.linspace(0, len(song), len(song)//1764, dtype = "int")

    all_freq_data = pd.DataFrame(columns = samples)

    for i, sample in enumerate(samples[:-1]):
      print(song[samples[i]:samples[i+1]])
      freq_data, freq_space = make_freq_spread(song[samples[i]:samples[i+1]],sr, True)
      all_freq_data[sample] = pd.Series(l.amplitude_to_db(freq_data))
      plt.show()
      plt.ylabel('Magnitude of signal')
      plt.xlabel('Frequency (Hz)')
    
    # all_freq_data.to_csv("all_freq_data.csv")

  if DISPLAY: 
    plt.show()
    plt.ylabel('Magnitude of signal')
    plt.xlabel('Frequency (Hz)')
  
if __name__ == "__main__":
    main()