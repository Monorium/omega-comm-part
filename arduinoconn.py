# coding: utf-8
from machine import UART
from time import sleep
from _thread import start_new_thread

class ArduinoTele():
    def __init__(self):
        self.clear()

    def clear(self):
        self.data = ""
        self.isRecving = False

class ArduinoConn():
    _STX = 0x02
    _ETX = 0x03

    def __init__(self, id=2, baud=115200):
        self._uart = UART(id, baud)
        self._recvCallback = None

    def init(self, txPin=None, rxPin=None):
        self._uart.init(tx=txPin, rx=rxPin)

    def startRecvThread(self, callback):
        start_new_thread(self._recv, callback)

    def send(self, message):
        buf = bytearray(chr(ArduinoConn._STX)) + bytearray(message.encode()) + bytearray(chr(ArduinoConn._ETX))
        self._uart.write(buf)

    def _recv(self, callback):
        tele = ArduinoTele()
        while True:
            while self._uart.any():
                buf = self._uart.read(1)
                if buf[0] == ArduinoConn._STX:
                    tele.clear()
                    tele.isRecving = True
                elif buf[0] == ArduinoConn._ETX:
                    callback(tele)
                    tele.clear()
                elif tele.isRecving:
                    tele.data += buf.decode()
                sleep(0.001)
            else:
                sleep(0.1)
