@echo off

set AMPY_PORT=COM5
ampy put boot.py
ampy put main.py

ampy put microWebSrv.py
ampy put microWebSocket.py

ampy put wifiman.py
ampy put network.json
ampy put omegaWebApp.py
ampy put arduinoconn.py
ampy put servo.py

pause
@echo on
