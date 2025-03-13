import network
from time import sleep

def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconected():
        print("Connecting.....")
    print("Connected @ IP: ",wlan.igconfig()[0])


