import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

# Wiring and connecting
button = Pin(12, Pin.IN, Pin.PULL_UP)
i2c=I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


#Displaying texts
oled.fill(0)
oled.text('Hello world', 20, 25, 1)
oled.show()

oled.fill(0)
oled.text('Press button', 15, 10, 1)

#Button check Loop
while button() == 1:
    time.sleep(0.05)

# Display update
oled.show()

#Drawing loop
x = 0
colour = 1
update = False

while True:
    if button() == 0:
        # Draws a line from x-axis, y-axis is set to 35, and what color
        oled.pixel(x, 35, colour)
        
        # update rate. the lower number the more it updates, the slower drawing
        if x % 8 == 0:
            oled.show()
            
        # pixels added (space between pixels)
        x += 1
        
        # If line reaches max width
        if x >= 128:
            
            # it starts to draw from min width
            x = 0
            
            # colour = colour ^ 1
            # idk how to use ^1 so I made it how I understands it
            colour = 1 - colour

    else:
        if update:
            update = False
            oled.show()
            