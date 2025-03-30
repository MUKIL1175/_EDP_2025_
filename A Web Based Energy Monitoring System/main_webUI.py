import network
import socket
import time
from machine import UART
from pzem import PZEM004Tv30
from wifi import wifi_connect

# Initialize UART and PZEM sensor
uart = UART(2, baudrate=9600, tx=17, rx=16)
pzem = PZEM004Tv30(uart)

# Connect to WiFi
wifi_connect("Pzem_004T", "1234567890")

# Create the HTML UI
html = """
<!DOCTYPE html>
<html>
<head>
  <title>PZEM-004T Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      background: radial-gradient(#0f0f0f, #050505);
      color: #fff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      position: relative;
    }
    h1 { color: #0ff; margin-bottom: 20px; }
    .btn {
      background: #1a1a1a;
      color: #0ff;
      border: 2px solid #0ff;
      border-radius: 10px;
      padding: 10px 20px;
      margin: 10px;
      font-size: 16px;
      cursor: pointer;
      box-shadow: 0 0 10px #0ff4;
    }
    .btn:hover {
      background: #0ff;
      color: #000;
    }
    .result {
      margin-top: 20px;
      font-size: 18px;
      color: #0ff;
    }
    .credit {
      position: fixed;
      bottom: 10px;
      right: 15px;
      font-size: 14px;
      color: #0ff8;
    }
  </style>
</head>
<body>
  <h1>PZEM-004T Live Data</h1>
  <button class="btn" onclick="fetchData('voltage')">Voltage</button>
  <button class="btn" onclick="fetchData('current')">Current</button>
  <button class="btn" onclick="fetchData('power')">Power</button>
  <button class="btn" onclick="fetchData('energy')">Energy</button>
  <button class="btn" onclick="fetchData('frequency')">Frequency</button>
  <button class="btn" onclick="fetchData('pf')">Power Factor</button>

  <div class="result" id="result">Click a button to get data.</div>

  <script>
    function fetchData(param) {
      fetch('/' + param)
        .then(res => res.text())
        .then(data => {
          document.getElementById('result').innerText = data;
        });
    }
  </script>
  <h3 class="credit">Coded and Designed by Mukil</h3>
</body>
</html>

"""

# Setup socket server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Listening on", addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)

    response = html

    try:
        if pzem.update():
            if '/voltage' in request:
                response = "Voltage: {} V".format(pzem.voltage())
            elif '/current' in request:
                response = "Current: {} A".format(pzem.current())
            elif '/power' in request:
                response = "Power: {} W".format(pzem.power())
            elif '/energy' in request:
                response = "Energy: {} kWh".format(pzem.energy())
            elif '/frequency' in request:
                response = "Frequency: {} Hz".format(pzem.frequency())
            elif '/pf' in request:
                response = "Power Factor: {}".format(pzem.pf())
        else:
            response = "Failed to read from PZEM sensor"
    except Exception as e:
        response = "Exception occurred"
        print("Error reading sensor:", e)

    except Exception as e:
        response = "Failed to read data"
        print("Error reading sensor:", e)

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
