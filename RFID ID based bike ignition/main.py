from read_uid import sending
from machine import Pin
from time import sleep
#Coded by Mukil
#Contact @ http://github/MUKIL1175
led = Pin(16, Pin.OUT)

stack = 1 

while True:
    print("Place the card")
    key = sending()

    if key in ["b3676027","73aef813"] and stack == 1:
        led.value(1); stack -= 1; sleep(0.5); print("relay OFF")
    else:
        led.value(0); stack += 1; sleep(0.5); print("relay ON")

