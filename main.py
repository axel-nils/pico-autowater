"""
Main program that automatically runs when Pico is powered
"""

import uasyncio as asyncio

import machine
import time

from devices import *
from utils import DataFile, WiFi, WIFI_NAME, WIFI_PASS, get_datetime, set_rtc


DATA_FILE = "data/data.json"

DRY_THRESHOLD, WET_THRESHOLD = 825, 850


class DataServer:
    def __init__(self, ip):
        self.ip = ip
        self.port = 80
        self.host = "0.0.0.0"

        self.files = {"html": "web/index.html", "error": "web/notfound.html",
                      "css": "web/style.css", "js": "web/app.js", "json": "data/data.json"}
        self.pages = self.preload_pages()

        self.water_on_off: bool = False
        self.moisture = None
        self.temp = None
        self.datetime = None

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
        html_requests = ["/", "/index.html", "/water_on?", "/water_off?"]

        print(f"Server got request \"{request}\"")

        if request == "/water_on?":
            self.water_on_off = True
        elif request == "/water_off?":
            self.water_on_off = False

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
        elif request == "/data/data.json":
            print("Server responding with JSON")
            header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n'
            response = self.pages["json"]

        return header, response

    def create_html_response(self):
        response = self.pages["html"]

        replacements = {"{temperature}": self.temp,
                        "{moisture}": self.moisture,
                        "{water_on_off}": self.water_on_off,
                        "{time_now}": self.datetime}
        for r in replacements:
            response = response.replace(r, str(replacements[r]))
        return response


async def update_slow():
    """
    Writes last measurement along with timestamp to file
    """
    while True:
        await asyncio.sleep(900)
        server.datetime = get_datetime()
        server.temp = sensor.temp
        server.moisture = sensor.mean_moisture()

        entry = data.Entry(server.datetime, server.moisture, server.temp)
        data.append_entry(entry)


async def update_fast():
    while True:
        await asyncio.sleep(10)
        sensor.update()


async def set_leds():
    while True:
        await asyncio.sleep(1)
        LED_ONBOARD.value(server.water_on_off)
        if sensor.dry():    # Water right away
            LED_RED.on()
            LED_GRN.off()
        elif sensor.wet():  # No need for water
            LED_RED.off()
            LED_GRN.on()
        else:               # Water if right time
            LED_RED.on()
            LED_GRN.on()


async def task_loop():
    loop = asyncio.get_event_loop()
    asyncio.create_task(asyncio.start_server(server.serve, server.host, server.port))
    asyncio.create_task(set_leds())
    asyncio.create_task(update_fast())
    asyncio.create_task(update_slow())
    loop.run_forever()


if __name__ == "__main__":
    wifi = WiFi(WIFI_NAME, WIFI_PASS)
    set_rtc()

    sensor: SoilSensor = SoilSensor(PIN_SCL, PIN_SDA, DRY_THRESHOLD, WET_THRESHOLD)
    data: DataFile = DataFile(DATA_FILE)
    server: DataServer = DataServer(wifi.ip)

    for n in range(3):
        LED_ONBOARD.on()
        time.sleep(0.2)
        LED_ONBOARD.off()
        time.sleep(0.2)

    try:
        asyncio.run(task_loop())
    finally:
        asyncio.new_event_loop()
        machine.reset()
