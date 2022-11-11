import library as lib

def main():
  
  INPUT_FILE = "../assets/365.wav" # audio input
  bot, mot, tot = lib.plot_volumes(INPUT_FILE)
  lib.draw_record_visual(bot, mot, tot)
  
if __name__ == "__main__":
    main()