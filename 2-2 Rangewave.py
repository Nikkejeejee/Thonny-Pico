from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

data = Filefifo(10, name='capture_250Hz_02.txt')

minv, maxv = 0, 0
for i in range(250 * 2): # Read 2s of data to find min and max values
    sample = data.get()
    if minv == 0 or sample < minv:
        minv = sample
    if maxv == 0 or sample > maxv:
        maxv = sample
        
print("Scaled values:")
time.sleep(1)

for j in range(250 * 10):  # 10 seconds of data
    sample = data.get()
    scaled_sample = (sample - minv) / (maxv - minv) * 100 # Value stays within 0-100 range
    print(max(0, min(scaled_sample, 100))) # Printing values
    
print(f"Min value: {minv}, Max value: {maxv}")


# OLED drawing plotter
oled.text('zzup betch', 20, 32, 1)
oled.show()

while True:
    sample = data.get()
    scaled_sample = (sample - minv) / (maxv - minv) * 64    # Scale sample value to fit OLED height
    scaled_sample = max(0, min(int(scaled_sample), 63)) 	# Ensure scaled value stays within 0-63 range
    oled.scroll(-1, 0)  									# Make the wave move in x-axis
    oled.pixel(125, 63 - scaled_sample, 1)  				# Positioning from the left = 125, 63-scaledsample
    oled.show()
