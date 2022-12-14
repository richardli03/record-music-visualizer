# import the CircuitPython board and busio libraries
import board
# Enable I2C (Qwiic) communication
from sparkfun_serlcd import Sparkfun_SerLCD_I2C
i2c = board.I2C()
serlcd = Sparkfun_SerLCD_I2C(i2c)

serlcd.set_backlight(10040319) # purple

# send command
serlcd.write("   Disco Diva   ")

# uncomment the following for the first run

# armsDown = [
# 	0b00100,
# 	0b01010,
# 	0b00100,
# 	0b00100,
# 	0b01110,
# 	0b10101,
# 	0b00100,
# 	0b01010]
# armsUp = [
# 	0b00100,
# 	0b01010,
# 	0b00100,
# 	0b10101,
# 	0b01110,
# 	0b00100,
# 	0b00100,
# 	0b01010]

# serlcd.create_character(1, armsUp)
# serlcd.create_character(0, armsDown)

# dancing dude
# while True:

# 		serlcd.set_cursor(1,0) # column, row
# 		serlcd.write_character(0) # print little man, arms down
# 		time.sleep(0.2)

# 		serlcd.set_cursor(1,0) # column, row
# 		serlcd.write_character(1) # print little man, arms up
# 		time.sleep(0.2)