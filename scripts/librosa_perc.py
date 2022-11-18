import librosa as l
import library as lib
import pandas as pd
import matplotlib.pyplot as plt

def main():
    INPUT_FILE = "../assets/365.wav" # audio input'
    
    y, sr = l.load(INPUT_FILE)
    y_harmonic, y_percussive = l.effects.hpss(y)
    lib.input_fps(y_harmonic, sr)  
    bot, mot, tot = lib.process(y_harmonic, False, sr)
    lib.plot_volume(bot, mot, tot)
    
    # lib.draw_record_visual(bot, mot, tot)
    
    # harmonic = pd.DataFrame(y_harmonic)
    # perc = pd.DataFrame(y_percussive)
    # harmonic.to_csv("harmonic.csv")
    # plt.show()
    

if __name__ == "__main__":
    main()