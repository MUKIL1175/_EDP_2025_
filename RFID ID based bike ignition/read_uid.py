from machine import Pin, SoftSPI
from mfrc522 import MFRC522
import utime

# ESP8266 safe pin configuration
SCK_PIN = 14   # D5
MOSI_PIN = 13  # D7
MISO_PIN = 12  # D6
RST_PIN = 5    # D1
CS_PIN = 4     # D2

# Create SPI object
spi = SoftSPI(baudrate=1000000, polarity=0, phase=0,
              sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))

# Create MFRC522 object using positional arguments
rc522 = MFRC522(SCK_PIN, MOSI_PIN, MISO_PIN, RST_PIN, CS_PIN, spi)

def read_uid():
    while True:
        (stat, tag_type) = rc522.request(rc522.REQALL)
        if stat == rc522.OK:
            (status, raw_uid) = rc522.SelectTagSN()
            if status == rc522.OK:
                rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(*raw_uid)
                print("Card detected! UID:", rfid_data)
                return str(rfid_data)
        utime.sleep(0.2)

def sending():
    return read_uid()


