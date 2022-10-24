from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq
# from pyAudioAnalysis import audioBasicIO as abi

# INPUT_FILE = "../pyAudioAnalysis/pyAudioAnalysis/data/doremi.wav"

INPUT_FILE = "../assets/365.wav"

WAVEFORM = False

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

s_rate, data = read(INPUT_FILE)
print(f"number of channels = {data.shape[1]}")

N = 600

length = data.shape[0] / s_rate
time = np.linspace(0., length, data.shape[0])

transformed_data = fft(data)

plt.plot(2.0/N * np.abs(transformed_data[0:N//2]))
plt.grid()      
plt.show()

if WAVEFORM:
    plt.plot(time, data[:, 0], label = "left")
    plt.plot(time, data[:, 1], label = "right")
    plt.legend()

    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.show()

