import network
from time import sleep


class WiFi:

    def __init__(self, ssid, psw, ip=None):
        """
        Initialize Wi-Fi connection by passing ssid and password.
        Use ip param to get specific ip-adress, otherwise ip is assigned by access point.
        """
        self.ssid = ssid
        self.psw = psw
        self.ip = ip
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.config(pm=0xa11140)  # Disable power saver-mode
        
        if not self.wlan.isconnected():
            self.attempt_connection()
        
        self.ip = self.wlan.ifconfig()[0]
        print(f"Connected to {ssid} with IP-address {self.ip}")

    def attempt_connection(self):
        if self.ip:
            self.wlan.ifconfig((self.ip, '255.255.255.0', '192.168.1.1', '192.168.1.1'))
        
        self.wlan.connect(self.ssid, self.psw)
        
        while not self.wlan.isconnected():
            print("Waiting for connection...")
            sleep(1)


if __name__ == "__main__":
    import ubinascii
    wifi = WiFi("mywifiname", "mywifipass")
    print(wifi.wlan.ifconfig())
    mac = ubinascii.hexlify(wifi.wlan.config('mac'), ':').decode()
    print(mac)
