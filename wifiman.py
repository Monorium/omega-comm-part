# coding: utf-8
import json
import network

_CONFIG_FILE = "network.json"
_CONFIG_KEY_IS_AP_MODE = "isApMode"
_CONFIG_KEY_AP = "ap"
_CONFIG_KEY_STA = "sta"
_CONFIG_KEY_SSID = "ssid"
_CONFIG_KEY_PASSWORD = "password"
_CONFIG_KEY_IP = "ip"
_CONFIG_KEY_SUBNET = "subnet"
_CONFIG_KEY_GATEWAY = "gateway"
_CONFIG_KEY_DNS = "dns"

_isApMode = False
_ssid = ""
_password = ""
_ip = ""
_subnet = ""
_gateway = ""
_dns = ""
_nic = ""

def start_wifi():
    """ Wi-Fi接続 """
    global _nic
    _load_config()
    if _isApMode:
        _nic = network.WLAN(network.AP_IF)
        _nic.active(True)
        _nic.ifconfig((_ip, _subnet, _gateway, _dns))
        _nic.config(essid=_ssid, password=_password)
    else:
        _nic = network.WLAN(network.STA_IF)
        _nic.active(True)
        _nic.connect(_ssid, _password)
        while not _nic.isconnected():
            pass

def _load_config():
    """ ネットワーク設定の読み込み """
    global _isApMode, _ssid, _password, _ip, _subnet, _gateway, _dns
    try:
        with open(_CONFIG_FILE, "r") as conf:
            config = json.loads(conf.read())
            print(config)
            _isApMode = config[_CONFIG_KEY_IS_AP_MODE]
            if _isApMode:
                _ssid = config[_CONFIG_KEY_AP][_CONFIG_KEY_SSID]
                _password = config[_CONFIG_KEY_AP][_CONFIG_KEY_PASSWORD]
                _ip = config[_CONFIG_KEY_AP][_CONFIG_KEY_IP]
                _subnet = config[_CONFIG_KEY_AP][_CONFIG_KEY_SUBNET]
                _gateway = config[_CONFIG_KEY_AP][_CONFIG_KEY_GATEWAY]
                _dns = config[_CONFIG_KEY_AP][_CONFIG_KEY_DNS]
            else:
                print(config[_CONFIG_KEY_STA])
                print(config[_CONFIG_KEY_STA][_CONFIG_KEY_SSID])
                _ssid = config[_CONFIG_KEY_STA][_CONFIG_KEY_SSID]
                _password = config[_CONFIG_KEY_STA][_CONFIG_KEY_PASSWORD]
    except Exception as e:
        print("config file load error. :" + e)
