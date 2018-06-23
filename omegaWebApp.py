# coding: utf-8
import json
from microWebSrv import MicroWebSrv
from arduinoconn import ArduinoConn
from servo import JointServo

webSrv = MicroWebSrv(webPath='www/')
arduino = ArduinoConn()
servoList = dict()

def _acceptWebSocketCallback(webSocket, httpClient):
    if httpClient._resPath == "/omega":
        webSocket.RecvTextCallback = _recvTextCallback
        webSocket.RecvBinaryCallback = _recvBinaryCallback
        webSocket.ClosedCallback = _closedCallback
    else:
        webSocket.Close()

def _recvTextCallback(webSocket, msg):
    print("WS RECV TEXT : %s" % msg)
    if msg == "ping":
        webSocket.SendText("ping")
    else:
        try:
            global arduino
            arduino.send(msg)
            webSocket.SendText("send ok")

        except Exception as e:
            print("error :" + e)
        except:
            print("unknown error")

def _recvBinaryCallback(webSocket, data):
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket):
    webSocket.Close()

def _recvArduino(tele):
    global servoList
    print("_recvArduino")

    try:
        jsonData = json.loads(tele.data)
        pin = jsonData["pin"]
        angle = jsonData["angle"]

        servo = None
        if pin in servoList:
            servo = servoList[pin]
            servo.move(angle)
        else:
            servo = JointServo(pin, angle)
            servoList[pin] = servo
    except Exception as e:
        print("error :" + e)


# Webサーバ起動
webSrv.WebSocketThreaded = True
webSrv.AcceptWebSocketCallback = _acceptWebSocketCallback
webSrv.Start(threaded=True)

# Arduino向けSerial通信開始
arduino.startRecvThread(_recvArduino)
