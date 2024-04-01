from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

while True:
    for i in range(1, 20): # because there are 24 frames
        file = open(f'/logo/img{i}.pbm', 'rb') # Reads file in binary = rb = ReadBinary
        file.readline()
        file.readline()
        dimensions = file.readline().split()  # Read dimensions
        width, height = int(dimensions[0]), int(dimensions[1])
        img = bytearray(file.read())
        file.close()  # Make sure to close the file
        gif = framebuf.FrameBuffer(img, oled_width, oled_height, framebuf.MONO_HLSB)
        oled.blit(gif, 0, 0)  # positioning gif
        oled.show()  # Shows animation
        time.sleep(0.00)  # Animation speed

