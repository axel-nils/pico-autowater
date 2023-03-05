"""
Main program that automatically runs when Pico is powered
"""

import urequests
import uasyncio as asyncio

from devices import *
from utils import DataDict, WiFi, WIFI_NAME, WIFI_PASS


DATA_FILE = "data/data.json"
TIME_API_URL = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"
DRY_THRESHOLD = 825
WET_THRESHOLD = 850


class DataServer:
    def __init__(self):
        wifi = WiFi(WIFI_NAME, WIFI_PASS)
        self.ip = wifi.ip
        self.port = 80
        self.host = "0.0.0.0"

        self.files = {"html": "web/index.html", "error": "web/notfound.html",
                      "css": "web/style.css", "js": "web/app.js"}
        self.pages = self.preload_pages()

        self.led_on_off = "OFF"
        self.moisture = None
        self.temp = None
        self.time = get_time()

    def preload_pages(self):
        pages = {}
        for name, file_name in self.files.items():
            with open(file_name, "r") as file:
                pages[name] = str(file.read())
        return pages

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
        response = self.pages["error"]
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
            response = self.pages["css"]
        elif request == "/app.js":
            print("Server responding with JS")
            header = 'HTTP/1.1 200 OK\r\nContent-Type: application/javascript\r\n\r\n'
            response = self.pages["js"]

        return header, response

    def create_html_response(self):
        response = self.pages["html"]
        time_now = get_time()

        replacements = {"{temperature}": self.temp,
                        "{moisture}": self.moisture,
                        "{led_on_off}": self.led_on_off,
                        "{time_now}": time_now}
        for r in replacements:
            response = response.replace(r, str(replacements[r]))
        return response


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


async def main():
    asyncio.create_task(asyncio.start_server(server.serve, server.host, server.port))
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


if __name__ == "__main__":
    sensor: SoilSensor = SoilSensor(PIN_SCL, PIN_SDA)
    data: DataDict = DataDict(DATA_FILE)
    server: DataServer = DataServer()

    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()
