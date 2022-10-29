import librosa as l
import librosa.display as disp
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as f
import pandas as pd


INPUT_FILE = "../assets/bass.wav"
# INPUT_FILE = "assets/365.wav"
DISPLAY = False
FREQ = True
 
song, sr = l.load(INPUT_FILE, mono = True)

def make_freq_plot(x, Fs, plot):
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

def make_time_plot(x, Fs):
    plt.plot(song)

def main():
  print(len(song))
  
  
  # freq_data, freq_space = make_freq_plot(song[:3000],sr)
  # len_samples = np.linspace(0, len(song), len(song)//1764)

  if FREQ:
    samples = np.linspace(0, len(song), len(song)//1764, dtype = "int")

    all_freq_data = pd.DataFrame(columns = samples)

    for i, sample in enumerate(samples[:-1]):
      print(song[samples[i]:samples[i+1]])
      freq_data, freq_space, sub1 = make_freq_plot(song[samples[i]:samples[i+1]],sr)
      all_freq_data[sample] = pd.Series(l.amplitude_to_db(freq_data))
    all_freq_data.to_csv("all_freq_data.csv")

  if DISPLAY: 
    plt.show()
    plt.ylabel('Magnitude of signal')
    plt.xlabel('Frequency (Hz)')
  
if __name__ == "__main__":
    main()