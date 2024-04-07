import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

down = Pin(9, Pin.IN, Pin.PULL_UP)    # SW0
left = Pin(8, Pin.IN, Pin.PULL_UP)    # SW1
up = Pin(7, Pin.IN, Pin.PULL_UP)      # SW2

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


# Setting dimensions. 56px is middle
y = oled_height // 2
x = 0

# Function to clear the OLED screen
def byebye():
    oled.fill(0)
    oled.show()


# get set ready!
byebye()
while True:
    oled.pixel(x, y, 1)				# Draws the line starting from left side of screen and line is in the middle
    oled.show()
    
    x += 1
    if x >= oled_width:
        x = 0						# Wrap around when reaching the right edge
    
    if down.value() == 0:
        y -= 1						# Move line up
        if y < 0:
            y = oled_height - 1		# Wrap around when reaching the top
    elif up.value() == 0:
        y += 1						# Move line down
        if y >= oled_height:
            y = 0					# Wrap around when reaching the bottom
    elif left.value() == 0:
        byebye()					# Clear screen and start drawing from left middle
        y = oled_height // 2
        x = 0
    
    time.sleep(0.05)				# Adjust delay as needed for desired drawing speed
