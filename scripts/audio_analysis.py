import library as lib

def main():
  
  INPUT_FILE = "../assets/mids.wav" # audio input
  lib.plot_volumes(INPUT_FILE)
  lib.create_csv()
  
if __name__ == "__main__":
    main()