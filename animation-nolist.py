from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

while True:
    for n in range(1, 28):
        with open('/youtube/image%s.pbm' % n, 'rb') as f:
            f.readline()  # Magic number
            f.readline()  # Creator comment
            dimensions = f.readline().split()  # Read dimensions
            width, height = int(dimensions[0]), int(dimensions[1])
            data = bytearray(f.read())
        
        fbuf = framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)
        
        for y in range(height):  # Adjust display if image height is smaller
            oled.fill_rect(0, y, width, 1, 0)
        
        oled.blit(fbuf, (oled_width - width) // 2, (oled_height - height) // 2)
        oled.show()
        time.sleep(0.01)  # Adjust sleep time as needed
