from machine import Pin
import time

btn = Pin(7, Pin.IN, Pin.PULL_UP)
alrm = Pin(9, Pin.IN, Pin.PULL_UP)
red_pin = Pin(22, Pin.OUT)
siren_pin = Pin(20, Pin.OUT)

siren = False
red = False
active = False
know = False  # values set to 0

while True:
    alarm = alrm.value()
    button = btn.value() == 0  # Button is pressed

    if alarm and not active:  # Alarm activated = led on
        active = True
        siren = True
        red = True
    
    if know and active:  # Blinking red light after acknowledgment
        red = not red

    if button and active and not know:  # Alarm deactivated before button pressed
        know = True
        siren = False
        red = True

    if not alarm and not know and active:  # Alarm deactivated before acknowledgment
        siren = False
        red = True

    if not alarm and know:  # Alarm deactivated after acknowledgment
        siren = False
        red = False
        active = False
        know = False

    siren_pin.value(siren)
    red_pin.value(red)  # Sets LED to boolean

    time.sleep(0.1)

