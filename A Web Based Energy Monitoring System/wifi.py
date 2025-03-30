import network
import time

def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Connecting...")
    
    print("Connected to WiFi!")
    print("IP Address:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]
