import network
from time import sleep


class WiFi:
    MAX_WAIT = 10

    def __init__(self, ssid, psw):
        self.ip = None

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.config(pm=0xa11140)  # Disable power saver-mode
        self.wlan.connect(ssid, psw)

        while self.MAX_WAIT > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            self.MAX_WAIT -= 1
            print("Waiting for wifi connection...")
            sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError("Wifi connection failed")
        else:
            self.ip = self.wlan.ifconfig()[0]
            print(f"Connected to {ssid} with IP-address {self.ip}")


if __name__ == "__main__":
    from utils import WIFI_NAME, WIFI_PASS
    wifi = WiFi(WIFI_NAME, WIFI_PASS)
    print(wifi.wlan.ifconfig())
