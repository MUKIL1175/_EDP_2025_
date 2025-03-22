from machine import ADC, Pin, I2C
import time
from ssd1306 import SSD1306_I2C
#Coded by Mukil follow us on github https://github.com/MUKIL1175
mq3_pin = ADC(Pin(26))  
ROTTEN_THRESHOLD = 50000  # test and cahnge it
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)
oled.text("Welcome",40,0);
oled.text("Initializing ......",0,20)
oled.show();time.sleep(5);oled.fill(0)
oled.text("Setup 100%",25,20)
oled.show()
time.sleep(2)

def read_mq3():
    return mq3_pin.read_u16()

def check_fruit_status(value):
    if value > ROTTEN_THRESHOLD:
        return "ROTTEN 🍌"
    else:
        return "FRESH ✅"

while True:
    mq3_value = read_mq3()
    status = check_fruit_status(mq3_value)

    print(f"MQ3 Reading: {mq3_value} | Status: {status}")

    oled.fill(0)
    oled.text("MQ3 Gas Sensor", 0, 0)
    oled.text("Value: " + str(mq3_value), 0, 20)
    oled.text("Status:", 0, 40)
    oled.text(status, 60, 40)
    oled.show()

    time.sleep(2)
