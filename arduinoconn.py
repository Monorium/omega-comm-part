# coding: utf-8
from machine import UART
import select
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

    @staticmethod
    def _startRecvThread(func, args):
        print("_startRecvThread")
        start_new_thread(func, args)

    def __init__(self, id=2, baud=115200):
        self._uart = UART(id, baud)

    def init(self, txPin=None, rxPin=None):
        self._uart.init(tx=txPin, rx=rxPin)

    def startRecvThread(self, callback):
        print("startRecvThread")
        ArduinoConn._startRecvThread(self._recv, (callback,))
        print("startRecvThread end")

    def send(self, message):
        buf = bytearray(chr(ArduinoConn._STX)) + bytearray(message.encode()) + bytearray(chr(ArduinoConn._ETX))
        self._uart.write(buf)

    def _recv(self, callback):
        tele = ArduinoTele()
        poller = select.poll()
        poller.register(self._uart, select.POLLIN)

        while True:
            events = poller.poll()
            print('events =', events)
            while self._uart.any():
                buf = self._uart.read(1)
                print(buf)
                if buf[0] == ArduinoConn._STX:
                    print("-> STX")
                    tele.clear()
                    tele.isRecving = True
                elif buf[0] == ArduinoConn._ETX:
                    print("-> ETX")
                    if tele.isRecving:
                        print(tele.data)
                        callback(tele)
                        tele.clear()
                elif tele.isRecving:
                    tele.data += buf.decode()
