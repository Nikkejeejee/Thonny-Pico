from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

down = Pin(9, Pin.IN, Pin.PULL_UP)	# SW0
bye = Pin(8, Pin.IN, Pin.PULL_UP)	# SW1
up = Pin(7, Pin.IN, Pin.PULL_UP)	# SW2

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

x = 0
y = oled_height // 2				# setting dimensions, // 2 cuts height in half

def byebye():						# press sw1 clears the screen
    oled.fill(0)
    oled.show()

# Get Set READY!
byebye()
while True:
    oled.pixel(x, y, 1)				# Draws a line starting from left side of screen and line is in the middle
    oled.show()						# Displays line
    x += 1							# Drags the line lika worm (from 0 to 128)
    
    if x >= oled_width:
        x = 0						# Goes back to the start when it exceeds 128px
    elif up() == 0:					# press sw2, line go up by 1px (minus because 0 is top of the screen)
        y -= 1
        if y < 0:
            y = oled_height			# If it goes below 0 it starts from the bottom
    elif down() == 0:
        y += 1						# press sw0, line go down (plus because 64 locates at the bottom)
        if y >= oled_height:
            y = 0					# if it exceeds 64px then it starts from the top
    elif bye() == 0:
        byebye()
        x = 0
        y = oled_height // 2		# sets it back to start otherwise it keeps running like a bug 
