import library as lib

def main():
  
  INPUT_FILE = "../assets/bass.wav" # audio input
  bot, mot, tot = lib.process(INPUT_FILE, False)
  # lib.plot_volume(bot, mot, tot)
  data = lib.draw_record_visual(bot, mot, tot)
  data.to_csv('pos_data.csv')

  # next steps: make pos_data go from -1 to 1 instead of where it is (which is using less of that range).
  #     figure out what's going on with oscillations
  
if __name__ == "__main__":
    main()
