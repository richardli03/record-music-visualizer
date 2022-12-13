import library as lib
import argparse
import json


def make_parser():
    """
    Creates a ArgumentParser object for CLI.
    """
    p = argparse.ArgumentParser(
        description="Some customizability options for our audio processing workflow!")

    p.add_argument(
        "-n", help="name of the test you'd like to run in the configuration file")
    
    p.add_argument(
        "-d", help="use existing dataset to reduce runtime", action = "store_true")

    p.add_argument(
        "-p", help="plot record and audio plots", action="store_true")

    return p
  
def main():
  """
  Runs the audio analysis pipeline

  Returns:
      data (pandas dataframe): A dataframe containing movement information
        for stepper motors. Additionally is written to a csv in the drivers folder.
  """
  bot, mot, tot, dataset_path = lib.process(NAME_OF_TEST, INPUT_FILE, FROM_CSV)
  
  if dataset_path != "":
    with open("../assets/config.json", "r") as config_file:
      write_config = json.load(config_file)
 
    write_config[NAME_OF_TEST]["song_data"] = dataset_path
    
    with open("../assets/config.json", "w") as config_file:
      json.dump(write_config, config_file, indent = 4, sort_keys= True)
  
  lib.plot_volume(bot, mot, tot)
  data = lib.create_record_visual_data(bot, mot, tot, PLOT)
  data.to_csv(f'../drivers/datasets/{NAME_OF_TEST}.csv')
  return data

  
if __name__ == "__main__":
  parser = make_parser()
  args = parser.parse_args()

  NAME_OF_TEST = args.n.lower()
  PLOT = args.p
  FROM_CSV = args.d
  
  with open("../assets/config.json") as config_file:
      config = json.load(config_file)[NAME_OF_TEST]
      print(f"your configuration: {config}")
  
  INPUT_FILE = config["audio"]
  
  if FROM_CSV:
    CSV_PATH = config["song_data"]
    if CSV_PATH == "":
      print("no CSV found, continuing with processing")
      FROM_CSV = False
    
  main()
