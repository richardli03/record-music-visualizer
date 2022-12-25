# Assets

This folder is split into 3 sub-folders:

## Datasets

When the user runs an audio file, they have the option of choosing to run it from an existing dataset instead of processing the song. This is only possible if that dataset has already been generated and added to this folder (this is done automatically if the dataset doesn't exist)

## IMGs

This folder contains some images that showcase the results of running the audio analysis workflow on various songs as well as some earlier images that represent a log of our work.

## Songs

This folder contains the wav files that allow us to process audio and visualize it! 


Finally, there's a `config.json` file in here that contains some of the data regarding the songs that makes it easier for a user to run our workflow. Instead of needing to change any constants in code, they can simply add their song to the configuration file and run it using the command line tools in `scripts/audio_analysis.py`. Here are a couple of notes regarding the configuration file:
- song_length is in seconds
- song_data is a path to the csv that we'll use in visualization