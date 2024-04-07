from machine import UART, Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# short for height cuz im lazy
h = 0

while True:
    name = input('Enter name: ')
    oled.text(name, 0, h, 1)						# prints the name on screen
    h += 8											#adds a new line for the next name
    oled.show()										# displays name here bc then it will leave a gap on the bottom of screen
    if h >= oled_height:							# condition if name exceeds the screen height
        oled.scroll(0, -8)							# scrolls the list by 8 pixels
        h = oled_height - 8							# new value to height when screen is full of names
        oled.fill_rect(0, h, oled_width, 8, 0)		#This will cover the previous names by 8 px. this way the ram doesn't fill up