import os

class GlobalConfig(object):
    PROJECT_FOLDER = os.path.abspath(os.path.dirname(__file__))

class ApiConfig(object):
    SECRET_KEY = "L-Jybu4f$-+d>qmT#~a7u*L_QE]xFs"

class AccessPointConfig(object):
    # Access Point
    INTERFACE = "uap0"
    SSID = os.getenv("AP_SSID", "raspi-hotspot")
    PASS = os.getenv("AP_PASS", "rpipass8*")
    IP = os.getenv("AP_IP", "192.168.27.1")
    IP_BASE = ".".join(IP.split(".")[:-1])
    CHANNEL = os.getenv("AP_CHANNEL", "6")
    DHCP_RANGE_START = int(os.getenv("AP_DHCP_RANGE_START", 2))
    DHCP_RANGE_END = int(os.getenv("AP_DHCP_RANGE_END", 100))
    DHCP_DURATION = os.getenv("AP_DHCP_DURATION", "12h")
    DHCP_RANGE = "{}.{},{}.{},{}".format(IP_BASE, DHCP_RANGE_START, IP_BASE, DHCP_RANGE_END, DHCP_DURATION)

class WifiConfig(object):
    # Access Point
    INTERFACE = "wlan0"
