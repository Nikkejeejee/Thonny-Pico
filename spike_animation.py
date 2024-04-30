# Code from https://thepihut.com/blogs/raspberry-pi-tutorials/micropython-skill-builders-8-oled-display-graphics
# Modified by me, fixed by ChatGPT lol

import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
width = 128
height = 64
oled = SSD1306_I2C(width, height, i2c)

def draw_spike_animation():
    while True:
        oled.fill(0)
        oled.text("spikey", 5, 0, 1)
        oled.hline(0, height - 1, width, 1)  # Draw a horizontal line
        
        # Draw the spike
        for i in range(0, height, 8):
            oled.line(63, height - i, width - i, 63, 1)  # Diagonal line
            oled.line(63, height - i, i, 63, 1)  # Diagonal line
            oled.vline(63, height - i, i, 1)  # Vertical line
        
            oled.show()
            time.sleep(0.03)  # Animation speed

        time.sleep(0.5)  # Add a longer delay before restarting the animation

draw_spike_animation()
