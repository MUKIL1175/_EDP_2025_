from machine import Pin, ADC, I2C
import time
import dht
import ssd1306

#contact mukil11ss@gmail.com
#This code is to monitor the air quality

mq3 = ADC(Pin(26))
dht11 = dht.DHT11(Pin(22))

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.text("WELCOME",35,0)
oled.text("Air Quality", 20, 20)
oled.text("Monitor", 35, 30)
oled.text("(SM)",44,55)
time.sleep(1)
oled.show()
time.sleep(5)

def read_mq3():
    raw_value = mq3.read_u16()  
    gas_level = (raw_value / 65535) * 100 
    return round(gas_level, 2)

def read_dht11():
    try:
        time.sleep(0.1)
        dht11.measure()
        temp = dht11.temperature()
        humidity = dht11.humidity()
        return temp, humidity
    except:
        return None, None

def update_display():
    time.sleep(0.1)
    oled.fill(0)  
    oled.text("Air Quality", 20, 0)
    oled.text("Monitor", 35, 15)
    temp, humidity = read_dht11()
    if temp is not None:
        oled.text(f"Temp: {temp} C", 0, 20)
        oled.text(f"Humidity: {humidity}%", 0, 30)
    else:
        oled.text("DHT11 Error!", 0, 30)
        
    gas_level = read_mq3()
    oled.text(f"Gas Level: {gas_level}%", 0, 50)
    oled.show()

while True:
    update_display()
    time.sleep(2)  
