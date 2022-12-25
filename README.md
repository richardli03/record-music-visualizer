# record-music-visualizer
Authors: Richard Li, Kat Canavan, Isha Goyal

A music visualizer inspired by a record player. The organization of this repository is split as follows. Check out [our website](https://olincollege.github.io/pie-2022-03/disco-divas/) which explains how we made this music visualizer in more detail.

## Assets

This folder contains the wav files that we process in our audio analysis workflow and the datasets that are generated (so that future generations with that song can use the csv instead of having to process the entire song). It additionally poses some images that we used to debug and showcase a log of our work. Check out the [README](assets/README.md) in this folder for a more in-depth explanation!

## Drivers

This folder contains all of the python code that we ran on the Raspberry Pi for our system. Specifically, the `main.py` file takes in a dataset + song long length and commands the system to move the DC and stepper motors such that they visualize the song.

## Firmware

This folder contains the Arduino C code that the Arduino uses to control the DC and Stepper Motors. 

## Scripts

This folder contains the python script `audio_analysis.py` that analyzes a song and returns a CSV that our driver script can use to generate a song visualization. `audio_analysis.py` utilizes the configuration file in `assets/` to dynamically perform analysis on different songs depending on the user's commands to the command line. The flags and corresponding functionality can be found by running `audio_analysis.py -h`

## Audio Processing 

We are creating an audio analysis suite from scratch using FFTs (Fast Fourier Transforms) over stretches of time.
Only dependences are NumPy, Pandas, Librosa, and Matplotlib

To run the audio processing, cd into `scripts` and run `python3 audio_analysis.py`
