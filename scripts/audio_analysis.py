import library as lib

def main():
  
  INPUT_FILE = "../assets/mids.wav" # audio input
  bot, mot, tot = lib.process(INPUT_FILE, True)
  lib.draw_record_visual(bot, mot, tot)
  
if __name__ == "__main__":
    main()