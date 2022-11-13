import library as lib

def main():
  
  INPUT_FILE = "../assets/365.wav" # audio input
  bot, mot, tot = lib.process(INPUT_FILE, True)
  lib.plot_volume(bot, mot, tot)
  # lib.draw_record_visual(bot, mot, tot)
  
if __name__ == "__main__":
    main()
