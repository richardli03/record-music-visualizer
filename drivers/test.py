"""
turn the DC motor on and spin the servo for a few seconds
"""

import time
import send_serial

# dc motor speed 200
send_serial.dc_speed(200)

# stepper motor

rotations = range(10)
for rotation in rotations:
    if (rotation%2)==0:
        # even
        send_serial.stepper('a', 45)
        time.sleep(1)
    else:
        # odd
        send_serial.stepper('a', -45)
        time.sleep(1)

# close_time = time.time() + 15   # close loop after 15 sec
# while time.time()<close_time:
#     send_serial.stepper('a', 90)
#     send_serial.stepper('a', -90)

# dc motor stop
send_serial.dc_off()