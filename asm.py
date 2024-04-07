from machine import Pin
import time

btn = Pin(7, Pin.IN, Pin.PULL_UP)
led = Pin(20, Pin.OUT)

ground = 1  # grounding button
lamp = 0  # LED is off

while True:
    btn_state = btn.value() # because int isn't callable
    if btn_state == 0 and ground == 1:  # button pressed
        lamp = 1 - lamp  # light either switches on or off
        led.value(lamp)
        time.sleep(0.05) # 50 ms period
    ground = btn_state
