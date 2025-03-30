import time
from machine import UART

class PZEM004Tv30:
    def __init__(self, uart, addr=0xF8):
        self.uart = uart
        self.addr = addr
        self.last_read = time.ticks_ms()
        self.values = {}

    def _send_command(self, command, register=0x0000, value=0x0000):
        frame = bytearray(8)
        frame[0] = self.addr
        frame[1] = command
        frame[2] = (register >> 8) & 0xFF
        frame[3] = register & 0xFF
        frame[4] = (value >> 8) & 0xFF
        frame[5] = value & 0xFF
        crc = self._crc16(frame[:6])
        frame[6] = crc & 0xFF
        frame[7] = (crc >> 8) & 0xFF
        self.uart.write(frame)

    def _read_response(self, length=25):
        start = time.ticks_ms()
        while self.uart.any() < length:
            if time.ticks_diff(time.ticks_ms(), start) > 1000:
                return None
            time.sleep(0.01)
        resp = self.uart.read(length)
        if not resp or len(resp) < length:
            return None
        if not self._check_crc(resp):
            return None
        return resp

    def _crc16(self, data):
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def _check_crc(self, data):
        crc = self._crc16(data[:-2])
        received = data[-2] | (data[-1] << 8)
        return crc == received

    def update(self):
        self._send_command(0x04, 0x0000, 0x000A)
        resp = self._read_response(25)
        if resp is None:
            return False

        self.values['voltage']   = ((resp[3] << 8) + resp[4]) / 10.0
        self.values['current']   = ((resp[5] << 8) + resp[6] + (resp[7] << 24) + (resp[8] << 16)) / 1000.0
        self.values['power']     = ((resp[9] << 8) + resp[10] + (resp[11] << 24) + (resp[12] << 16)) / 10.0
        self.values['energy']    = ((resp[13] << 8) + resp[14] + (resp[15] << 24) + (resp[16] << 16)) / 1000.0
        self.values['frequency'] = ((resp[17] << 8) + resp[18]) / 10.0
        self.values['pf']        = ((resp[19] << 8) + resp[20]) / 100.0
        return True

    def voltage(self):
        return self.values.get('voltage', float('nan'))

    def current(self):
        return self.values.get('current', float('nan'))

    def power(self):
        return self.values.get('power', float('nan'))

    def energy(self):
        return self.values.get('energy', float('nan'))

    def frequency(self):
        return self.values.get('frequency', float('nan'))

    def pf(self):
        return self.values.get('pf', float('nan'))
