import library as lib

def main():
  
  INPUT_FILE = "../assets/bass.wav" # audio input
  bot, mot, tot = lib.process(INPUT_FILE, False)
  lib.plot_volume(bot, mot, tot)
  data = lib.draw_record_visual(bot, mot, tot)

  print(data)
  
if __name__ == "__main__":
    main()
