'''
Implement a program that uses the rotary encoder to control LED brightness. The encoder button is used to toggle the LED on/off and turning the encoder adjusts the brightness if the LED is on-state. If the LED is off, then the encoder turns are ignored. The program must use interrupts for detecting encoder turns and a fifo to communicate turns to the main program. The interrupt handler may not contain any LED handling logic. Its purpose is to send turn events to the main program.
The encoder button must be polled in the main program and filtered for switch bounce.

'''
from machine import Pin
from fifo import Fifo
from led import Led
import time

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, Pin.IN, Pin.PULL_UP)
        self.b = Pin(rot_b, Pin.IN, Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        
    def handler(self, pin):
        if self.b.value():
            self.fifo.put(-5)
        else:
            self.fifo.put(5)
            
class Button:
    def __init__(self, sw):
        self.push = Pin(sw, Pin.IN, Pin.PULL_UP)
        self.prev = 1  # Previous state
        
    def press(self):
        cur = self.push.value()  # current state
        if cur != self.prev and cur == 0:  # Checks if button is not pressed and if it's pressed
            self.prev = cur
            return True  # button is pressed
        self.prev = cur
        return False  # button not pressed
        
rot = Encoder(10, 11)
led = Led(22)
button = Button(12)
bright = 1

while True:
    if rot.fifo.has_data():
        if led.value():  # Check if LED is on
            bright += rot.fifo.get()
            bright = min(100, max(0, bright))
            led.brightness(bright)
        else:
            rot.fifo.get()
            
    if button.press():
        led.toggle()

    time.sleep(0.01)  # Debounce delay

