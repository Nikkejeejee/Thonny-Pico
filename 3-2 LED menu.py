'''
Implement a program that uses the rotary encoder to last an item from a menu. The menu has three options: LED1, LED2, LED3. Encoder turns move the lastion (arrow, highlight, etc.) and pressing the button activates the lastion. Activation turns toggles the lasted LED on/off. The state of the LED must be updated in the menu. Use an interrupt for both turn detection and encoder button. The turn and press event must be sent to the main program through a fifo. All of the menu logic must be in the main program.
The encoder button does not have hardware filtering so switch bounce filtering must be performed. Bounce filtering should be done in the interrupt handler with the help of time.ticks_XXX-functions. Filtering is done by taking a millisecond time stamp on each detected press and comparing that to the timestamp of previous press. The new press is ignored if it is too close, for example less than 50 ms away from the previous press.
'''
from machine import Pin, I2C
from fifo import Fifo
from led import Led
from ssd1306 import SSD1306_I2C
import micropython, time

micropython.alloc_emergency_exception_buf(200)


class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, Pin.IN, Pin.PULL_UP)
        self.b = Pin(rot_b, Pin.IN, Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.last = 0  # Stores the last pressed time
        self.debounce = 50  # Adjust this value for debounce time (milliseconds)

    def handler(self, pin):
        cur_time = time.ticks_ms()
        if cur_time - self.last >= self.debounce:
            if self.b():
                self.fifo.put(-1)
            else:
                self.fifo.put(1)
            self.last = cur_time

class Button:
    def __init__(self, sw):
        self.push = Pin(sw, Pin.IN, Pin.PULL_UP)
        self.prev = 1  # previous state, grounded
        self.prior = 0  # last time the button was pressed

    def press(self):
        cur = self.push.value()
        cur_time = time.ticks_ms()
        
        if cur != self.prev and cur == 0:  # Checks if button is pressed or not
            if cur_time - self.prior >= 50:  # Check if debounce time has passed (50 ms)
                self.prev = cur
                self.prior = cur_time
                return True  # button is pressed
        self.prev = cur
        return False  # button NOT pressed

class Screen:
    def __init__(self, option):
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.w = 128  # stands for width cuz im lazy
        self.h = 64
        self.oled = SSD1306_I2C(self.w, self.h, self.i2c)
        self.y = self.h//3
        self.option = option
        self.last = 0
        self.state = [False] * len(option)  # Initialize all LEDs to off

    def menu(self):
        self.oled.fill(0)
        for nro, item in enumerate(self.option):
            if self.state[nro]:  # Check if led is on
                status = "ON"
            else:
                status = "OFF"
            letterw = len(status) * 8  # Calculate the width of the text based on its length
            # displays LED num and state
            if nro == self.last:
                self.oled.text(item, 10, self.y * nro, 1)
                self.oled.text('>', 0, self.y * nro, 1)
            else:
                self.oled.text(item, 10, self.y * nro, 1)
            self.oled.text(status, self.w - letterw, self.y * nro, 1)  # display on/off
        self.oled.show()

rot = Encoder(10, 11)
button = Button(12)
leds = [Led(22), Led(21), Led(20)]
menu = Screen(['LED 1', 'LED 2', 'LED 3'])

while True:
    if rot.fifo.has_data():
        rotation = rot.fifo.get()
        print(rotation)  # print on shell
        
        menu.last = max(0, min(menu.last + rotation, 2)) # icon moves within range of 0-2
        menu.menu()  # Updates display

    if button.press():
        pick = menu.last
        state = not menu.state[pick]  # Toggling LED state, boolean is stored in state variable.
        menu.state[pick] = state  # Update state text
        leds[pick].value(state)  # Turn on/off the corresponding LED
        menu.menu()
