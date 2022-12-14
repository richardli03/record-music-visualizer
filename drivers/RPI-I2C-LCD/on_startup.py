import socket # for ip
import board # import the CircuitPython board and busio libraries
from sparkfun_serlcd import Sparkfun_SerLCD_I2C # Enable I2C (Qwiic) communication

i2c = board.I2C()
serlcd = Sparkfun_SerLCD_I2C(i2c)
serlcd.set_backlight(10040319) # purple

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address
 
serlcd.write('Ready to Disco?\n') 
serlcd.write(get_ip_address())

# uncomment the following to set a timer
# # Wait 5 seconds
# import time
# time.sleep(10.0)
# lcd.clear()