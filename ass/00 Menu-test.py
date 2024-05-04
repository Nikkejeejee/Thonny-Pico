# 3.5.2024 22pm draft

import time, framebuf, micropython
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo

# Classes from other files need to be imported here if they're used
from results_processor import record

micropython.alloc_emergency_exception_buf(200)

class Screen:
    def __init__(self):
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.width = 128
        self.height = 64
        self.display = SSD1306_I2C(self.width, self.height, self.i2c)
        self.padding = 10
        self.gap = 15

    def draw_menu(self, sector):
        self.display.fill(0)
        self.display.ellipse(int(self.width / 2), int(self.height / 2), 30, 30, 1, True, sector) # white quadrant
        self.display.ellipse(int(self.width / 2), int(self.height / 2), 25, 25, 0, True) # black small sircle
        self.display.ellipse(int(self.width / 2), int(self.height / 2), 30, 30, 1) # outer white circle (outlines)
        self.display.ellipse(int(self.width / 2), int(self.height / 2), 25, 25, 1) # inner white circle (outlines)

    def alignment(self, text, value, y_pos):
        text_width = len(text) * 8
        value_str = str(value)
        value_width = len(value_str) * 8
        
        if not text:  # if empty text or value
            text_width = 0
        if not value:
            value = "No value"
        
        text_x = self.padding
        value_x = self.width - len(value_str) * 8
        
        self.display.text(text, text_x, y_pos, 1)
        self.display.text(value_str, value_x, y_pos, 1)
        
    def display_results(self, results):
        self.display.fill(0)
        y_pos = self.padding

        for text, value in results:
            self.alignment(text, value, y_pos)
            y_pos += self.gap  # adds Y position for the next line

        self.display.show()

    def bpm(self, bpm_val):
        results = [("BPM:", bpm_val)]
        self.display_results(results)

    def hrv_dis(self, mean_hr, mean_ppi, rmssd, sdnn):
        results = [
            ("MEAN HR:", mean_hr),
            ("MEAN PPI:", mean_ppi),
            ("RMSSD:", rmssd),
            ("SDNN:", sdnn),
        ]
        self.display_results(results)

    def kubios_dis(self, mean_hr, mean_ppi, rmssd, sdnn, sns, pns):
        results = [
            ("MEAN HR:", mean_hr),
            ("MEAN PPI:", mean_ppi),
            ("RMSSD:", rmssd),
            ("SDNN:", sdnn),
            ("SNS:", sns),
            ("PNS:", pns),
        ]
        self.display_results(results)


class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)

        self.but = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
        self.last_rotation = time.ticks_ms()
        self.knob_fifo = Fifo(30, typecode="i")
        self.last_pressed = 0  # last time the button was pressed
        self.debounce = 500
        self.pressed = False

        self.fifo = Fifo(30, typecode="i")
        self.a.irq(handler=self.rot_handler, trigger=Pin.IRQ_RISING, hard=True)
        self.but.irq(handler=self.but_handler, trigger=Pin.IRQ_FALLING, hard=True)

    def rot_handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

    def but_handler(self, pin):
        button_press = time.ticks_ms()  # Get button pressed time in milliseconds
        if button_press - self.last_pressed > self.debounce:
            self.knob_fifo.put(1)
            self.last_pressed = button_press


oled = Screen()
encoder = Encoder(10, 11)

# Init encoder value and rotation
enc_value = 0b0001  # b0 for Q1
rotval = 0

# Init list for RRIs (R-R intervals)
rri_list = []  # Init RRI list here just in case Kubios is called before HRV analysis
# so that this works as an error catch

bpm_val = ';-;'

while True:
    # sphere graphics
    while encoder.fifo.has_data():
        rotval += encoder.fifo.get()
        if not encoder.pressed:  # This check here to not change menus when inside one
            print(rotval)
            if rotval > 3:  # so that Q doesn't change with minor knob movement
                rotval = 0
                enc_value >>= 1  # changing Q
                if enc_value == 0b0000:  # from Q1 to Q4
                    enc_value = 0b1000
            elif rotval < -3:
                rotval = 0
                enc_value <<= 1  # changing Q
                if enc_value == 0b10000:  # from Q4 to Q1
                    enc_value = 0b0001

    # Display menu
    oled.draw_menu(enc_value)
    if enc_value == 0b0001:
        icons.heart_icon()
    elif enc_value == 0b1000:  # 2nd selection
        icons.hrv_icon()
    elif enc_value == 0b0100:  # 3rd selection
        icons.kubios_icon()
    elif enc_value == 0b0010:
        icons.history_icon()

    # Check for encoder knob results
    if encoder.knob_fifo.has_data():
        encoder.pressed = True
        
        if enc_value == 0b0001:
            oled.bpm(bpm_val)
            print('bpm seleced')
            # BPM and heart curve
            # Init Andrei's code
            pass
        elif enc_value == 0b1000:
            print("HRV selected")
            rri_list = record_heart_rate()
            results_dict = basic_hrv_analysis(rri_list)
            print(results_dict)
            oled.hrv_dis(results_dict)
            # Call for the display function here with results dictionary
            pass
        elif enc_value == 0b0100:
            # Kubios
            # Pass list of RRIs (caught previously) to Andrei's Kubios stuff. If empty,
            # prompt user or do nothing
            # Returns analysis results as JSON, I think the drawing should be called here
            # and not directly from the Kubios code, but I don't know. It's WIP
            print("Kubios selected")
            if len(rri_list) == 0:
                print("Use HRV mode first")
            else:
                oled.kubios_dis()
            pass
        elif enc_value == 0b0010:
            print("History selected")
            # History
            # Call for history drawing things here. It handles its own display
            pass

    oled.display.show()
