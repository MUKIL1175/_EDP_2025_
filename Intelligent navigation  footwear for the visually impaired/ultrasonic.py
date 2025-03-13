from machine import Pin, time_pulse_us
import time

TRIG = Pin(5, Pin.OUT)  # Use GPIO5 (D1)
ECHO = Pin(4, Pin.IN)   # Use GPIO4 (D2)

def measure_distance():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    duration = time_pulse_us(ECHO, 1, 30000)
    if duration < 0:
        return None 
    distance = (duration * 0.0343) / 2  
    return distance
# 
# while True:
#     dist = measure_distance()
#     if dist is not None:
#         print("Distance:", dist, "cm")
#         time.sleep(1)
#     else:
#         print("Out of range")
#     time.sleep(0.1)  
