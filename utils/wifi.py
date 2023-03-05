import network
from time import sleep


class WiFi:
    MAX_WAIT = 10

    def __init__(self, ssid, psw):
        self.ip = None

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm=0xa11140)  # Disable power saver-mode
        wlan.connect(ssid, psw)

        while self.MAX_WAIT > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            self.MAX_WAIT -= 1
            print("Waiting for wifi connection...")
            sleep(1)

        if wlan.status() != 3:
            raise RuntimeError("Wifi connection failed")
        else:
            self.ip = wlan.ifconfig()[0]
            print(f"Connected to {ssid} with IP-address {self.ip}")
