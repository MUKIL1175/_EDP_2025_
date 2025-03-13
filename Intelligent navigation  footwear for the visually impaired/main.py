from machine import Pin
from time import sleep
from ultrasonic import measure_distance

led = Pin(2,Pin.OUT)
buzz = Pin(13,Pin.OUT)


def beep(dist):
    if dist <= 15 and dist >= 5:
        buzz.value(1);sleep(0.2)
    else:
        buzz.value(0)
    
while True:
    dist = measure_distance()
    if dist is not None:
        print("Distance:", dist, "cm")
        beep(dist)
        sleep(0.1)
    else:
        print("Out of range")
    sleep(0.1)
