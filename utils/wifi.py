import network
import urequests as requests
import time

from lib import uping


class WiFi:

    def __init__(self, ssid, psw, ip=None):
        """
        Initialize Wi-Fi connection by passing ssid and password.
        Use ip param to get specific ip-adress, otherwise ip is assigned by access point.
        """
        self.ssid = ssid
        self.psw = psw
        self.ip = ip
        network.country("SE")  # To comply with swedish redio regulations
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.config(pm=0xa11140)  # Disable power saver-mode

        self.attempt_connection()
        print(f"Connected to {self.ssid} with IP-adress {self.ip}")

    def attempt_connection(self):
        if self.ip:
            self.wlan.ifconfig(
                (self.ip, '255.255.255.0', '192.168.1.1', '192.168.1.1'))

        if not self.wlan.isconnected():
            self.wlan.connect(self.ssid, self.psw)
            while not self.wlan.isconnected():
                print("Waiting for connection...")
                time.sleep(3)
                self.wlan.connect(self.ssid, self.psw)
        self.ip = self.wlan.ifconfig()[0]

    def test_connection(self):
        """Returns true if able to connect to url on the internet"""
        if not self.wlan.isconnected():
            return False
        try:
            sent, received = uping.ping("192.168.1.1", quiet=True)
            if sent != received:
                raise OSError("ping error")
        except OSError as e:
            print(e)
            return False
        else:
            return True


def main():
    while True:
        if wifi.test_connection():
            print("connection ok")
        else:
            print("connection not ok")
            wifi.attempt_connection()
        time.sleep(10)


if __name__ == "__main__":
    import ubinascii
    wifi = WiFi("wifiname", "wifipass")
    print(wifi.wlan.ifconfig())
    mac = ubinascii.hexlify(wifi.wlan.config('mac'), ':').decode()
    print(mac)
    main()
