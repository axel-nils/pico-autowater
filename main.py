"""
Main program that automatically runs when Pico is powered
"""
from machine import Pin
from time import sleep
import network
import urequests
import uasyncio as asyncio

from is_sensor import SoilSensor
from is_data import DataDict

from my_credentials import WIFI_NAME, WIFI_PSW

SCL_PIN = Pin(17)
SDA_PIN = Pin(16)
LED_GRN = Pin(11, Pin.OUT)
LED_RED = Pin(10, Pin.OUT)
LED_ONBOARD = Pin("LED", machine.Pin.OUT)

DATA_FILE = "data/data.json"
TIME_FILE = "data/backup_time.txt"
TIME_API_URL = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"
DATA_DELAY = 3600 * 1000  # Once per hour
UPDATE_DELAY = 1 * 1000   # Once every 10 seconds
DRY_THRESHOLD = 825
WET_THRESHOLD = 850


class DataServer:
    def __init__(self, max_wait=10, ssid=WIFI_NAME, pswd=WIFI_PSW):
        self.max_wait = max_wait
        self.ssid = ssid
        self.pswd = pswd

        self.html_file = "index.html"
        self.css_file = "style.css"
        self.error_file = "notfound.html"
        self.html = None
        self.css = None
        self.error_page = None
        self.preload_files()

        self.ip = None
        self.port = 80
        self.host = "0.0.0.0"

        self.connect()
        self.led_on_off = "OFF"
        self.moisture = None
        self.temp = None
        self.time = get_time()

    def preload_files(self):
        with open(self.html_file, "r") as file:
            self.html = str(file.read())
        with open(self.css_file, 'r') as file:
            self.css = str(file.read())
        with open(self.error_file, 'r') as file:
            self.error_page = str(file.read())

    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm=0xa11140)  # Disable power saver-mode
        wlan.connect(WIFI_NAME, WIFI_PSW)

        while self.max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            self.max_wait -= 1
            print("Waiting for connection...")
            sleep(1)

        if wlan.status() != 3:
            raise RuntimeError("Network connection failed")
        else:
            self.ip = wlan.ifconfig()[0]
            print(f"Connected to {WIFI_NAME} with IP-address {self.ip}")

    async def serve(self, reader, writer):
        request_line = await reader.readline()
        while await reader.readline() != b"\r\n":
            pass

        header, response = self.handle_request(request_line)
        writer.write(header)
        writer.write(response)
        await writer.drain()
        await writer.wait_closed()

    def handle_request(self, request_line):
        request = str(request_line)
        try:
            request = request.split()[1]
        except IndexError:
            pass

        header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
        response = self.error_page
        html_requests = ["/", "/index.html", "/lighton?", "/lightoff?"]

        print(f"Server got request \"{request}\"")

        if request == "/lighton?":
            LED_ONBOARD.on()
            self.led_on_off = "ON"
        elif request == "/lightoff?":
            LED_ONBOARD.off()
            self.led_on_off = "OFF"

        if request in html_requests:
            print("Server responding with HTML")
            header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
            response = self.create_html_response()
        elif request == "/style.css":
            print("Server responding with CSS")
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n'
            response = self.css

        return header, response

    def create_html_response(self):
        response = self.html
        time_now = get_time()

        replacements = {"{temperature}": self.temp,
                        "{moisture}": self.moisture,
                        "{led_on_off}": self.led_on_off,
                        "{time_now}": time_now}
        for r in replacements:
            response = response.replace(r, str(replacements[r]))
        return response

    async def run(self):
        asyncio.create_task(asyncio.start_server(self.serve, self.host, self.port))
        while True:
            sensor.update()

            if sensor.mean_moisture() < DRY_THRESHOLD:
                LED_RED.on()
                LED_GRN.off()
            elif sensor.mean_moisture() > DRY_THRESHOLD:
                LED_RED.off()
                LED_GRN.on()

            server.temp = sensor.temp
            server.moisture = sensor.mean_moisture()
            server.time = get_time()
            await asyncio.sleep(1)


def get_datetime_json():
    time_r = urequests.get(TIME_API_URL)
    time_j = time_r.json()
    time_r.close()
    return time_j


def get_time():
    d = get_datetime_json()
    return d["time"]


def data_tick():
    """
    Writes last measurement along with timestamp to file
    """
    # data.add(str(time), sensor.values())
    # data.save()


if __name__ == "__main__":
    sensor: SoilSensor = SoilSensor(SCL_PIN, SDA_PIN)
    data: DataDict = DataDict(DATA_FILE)
    server: DataServer = DataServer()

    try:
        asyncio.run(server.run())
    finally:
        asyncio.new_event_loop()
