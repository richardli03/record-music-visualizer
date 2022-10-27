import librosa as lbr
import librosa.display as disp
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE = "../assets/treble.wav"
DISPLAY = True
 
song, sr = lbr.load(INPUT_FILE)
# S = song
S = np.abs(lbr.stft(song))
chroma = lbr.feature.chroma_stft(S=S, sr=sr)
db = lbr.amplitude_to_db(S,ref=np.max)
fig, ax = plt.subplots(nrows=2, sharex=True)
img = disp.specshow(lbr.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
fig.colorbar(img, ax=[ax[0]])
ax[0].label_outer()
img = disp.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
fig.colorbar(img, ax=[ax[1]])
plt.show()