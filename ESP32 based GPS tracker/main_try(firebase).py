import network
import socket
import time
from machine import UART
import urequests

# Wi-Fi credentials
ssid = "gps_esp32"
password = "1234567890"

# Firebase Config
FIREBASE_URL = "https://gpsesp32-default-rtdb.firebaseio.com"
FIREBASE_PATH = "/esp32/gps_ip.json"

# Connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"Connecting to Wi-Fi: {ssid}")
        wlan.connect(ssid, password)
        timeout = time.time() + 15
        while not wlan.isconnected() and time.time() < timeout:
            time.sleep(1)

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print("Connected!")
        print("IP Address:", ip)
        return ip
    else:
        print("Wi-Fi connection failed.")
        return None

# Send IP to Firebase
def send_ip_to_firebase(ip):
    try:
        url = FIREBASE_URL + FIREBASE_PATH
        data = { "ip": ip }
        response = urequests.put(url, json=data)
        print("IP sent to Firebase:", response.text)
        response.close()
    except Exception as e:
        print("Failed to send IP to Firebase:", e)

# Parse GPRMC NMEA sentence
def parse_gprmc(sentence):
    parts = sentence.split(',')
    if parts[2] == 'A':
        raw_lat = parts[3]
        lat_dir = parts[4]
        raw_lon = parts[5]
        lon_dir = parts[6]

        def convert(coord, direction):
            if coord == '':
                return None
            deg = int(float(coord) / 100)
            minutes = float(coord) - deg * 100
            decimal = deg + minutes / 60
            if direction in ['S', 'W']:
                decimal = -decimal
            return round(decimal, 6)

        lat = convert(raw_lat, lat_dir)
        lon = convert(raw_lon, lon_dir)
        if lat is not None and lon is not None:
            return lat, lon
    return None

# Get GPS coordinates
def get_gps_coords(uart, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        if uart.any():
            line = uart.readline()
            try:
                line = line.decode('utf-8').strip()
                if line.startswith('$GPRMC'):
                    coords = parse_gprmc(line)
                    if coords:
                        return coords
            except:
                pass
    return None

# Web server
def start_web_server(ip, uart):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print(" Web server running at http://{}/".format(ip))

    try:
        while True:
            cl, addr = s.accept()
            print("Client connected:", addr)
            request = cl.recv(1024)

            coords = get_gps_coords(uart)
            if coords:
                lat, lon = coords
                maps_url = f"https://maps.google.com/?q={lat},{lon}"
                html = f"""
                <html>
                    <head>
                        <title>ESP32 GPS Tracker</title>
                        <meta http-equiv="refresh" content="10">
                        <style>
                            body {{ font-family: Arial; text-align: center; background: #f4f4f4; }}
                            h2 {{ color: #333; }}
                            iframe {{ border: none; width: 90%; height: 400px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.2); }}
                        </style>
                    </head>
                    <body>
                        <h2>Current GPS Location</h2>
                        <p><strong>Latitude:</strong> {lat}</p>
                        <p><strong>Longitude:</strong> {lon}</p>
                        <p><a href="{maps_url}" target="_blank">Open in Google Maps</a></p>
                        <iframe src="https://maps.google.com/maps?q={lat},{lon}&z=15&output=embed"></iframe>
                        <p style="color:#777;">Auto-refreshes every 10 seconds</p>
                    </body>
                </html>
                """
            else:
                html = """
                <html><body style="text-align:center; font-family: Arial;">
                    <h2>Waiting for GPS Fix...</h2>
                    <p>Please ensure GPS has clear sky visibility.</p>
                </body></html>
                """

            cl.send('HTTP/1.1 200 OK\r\n')
            cl.send('Content-Type: text/html\r\n')
            cl.send('Connection: close\r\n\r\n')
            cl.sendall(html)
            cl.close()
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        s.close()

# Main
ip = connect_wifi(ssid, password)
gps_uart = UART(2, baudrate=9600, tx=17, rx=16)

if ip:
    send_ip_to_firebase(ip)
    start_web_server(ip, gps_uart)
else:
    print(" Cannot start web server without Wi-Fi.")
