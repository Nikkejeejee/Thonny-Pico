import time
from machine import UART, Pin, I2C
from ssd1306 import SSD1306_I2C

down = Pin(9, Pin.IN, Pin.PULL_UP)				# Wiring sw0
left = Pin(8, Pin.IN, Pin.PULL_UP)				# sw1
up = Pin(7, Pin.IN, Pin.PULL_UP)				# Wirigng sw2
right = Pin(12, Pin.IN, Pin.PULL_UP)			# rotary knob
i2c=I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Setting dimentions. 56px indicates center
x = 56
y = 56
ufo_w = 8*3										# w=width
ufo_h = 8										# h=height


while True:
    if right() == 0:							# When pressed rotary knob UFO moves to right by 15px
        x += 15
        if x >= oled.width - ufo_w:				# Prevents ufo from disappearing
            x = oled.width - ufo_w
    elif left() == 0:							# sw_1 is pressed, ufo moves to left by 15px
        x -= 15
        if x <= 0:								# Max value to left 0 so that's why it's set to 0
            x = 0
    if up() == 0:
        y -= ufo_h
        if y <= 0:								# If yk yk
            y = 0
    elif down() == 0:
        y += ufo_h
        if y >= oled.height - ufo_h:
            y = oled.height - ufo_h
    oled.fill(0)
    oled.text('<=>', x, y, 1) 
    oled.show()									#displays UFO when conditions are met
    time.sleep(0.05)							# button sensitivity