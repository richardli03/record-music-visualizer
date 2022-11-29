import library as lib

def main():
  
  INPUT_FILE = "../assets/here's_to_us_halestorm.wav" # audio input
  bot, mot, tot = lib.process(INPUT_FILE, False)
  lib.plot_volume(bot, mot, tot)
  data = lib.create_record_visual_data(bot, mot, tot, True)
  data.to_csv('pos_data.csv')
  
if __name__ == "__main__":
    main()
