import library as lib
import numpy as np
import pandas as pd

def main():
  INPUT_FILE = "../assets/mids.wav" # audio input
  lib.input_file(INPUT_FILE)
  

  if FREQ:
    samples = np.linspace(0, song_length, int(song_length//num_samples), dtype = "int") # create a linspace for time (by sample)

    # creates dataframe with samples as column headers and frequencies as row headers
    all_freq_data = pd.DataFrame(columns = samples)

    # iterates through samples (time steps)
    for i, sample in enumerate(samples[:-1]):
      freq_data, freq_space = make_freq_spread(song[samples[i]:samples[i+1]], sr, False)
      all_freq_data[sample] = pd.Series(l.amplitude_to_db(freq_data))
      
  
    all_freq_data = pd.read_csv('all_freq_data.csv')
    bass_data, mid_data, treble_data = data_splitter(all_freq_data.fillna(value = -100))
    
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