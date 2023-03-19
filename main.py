"""
Main program that automatically runs when Pico is powered
"""

import uasyncio as asyncio

import machine
import time

from devices import *
from utils import Config, DataFile, WiFi, get_datetime, get_time, set_rtc, is_morning

DATA_FILE = "data/data.json"


class DataServer:
    def __init__(self, ip):
        self.ip = ip
        self.port = 80
        self.host = "0.0.0.0"

        self.files = {"html": "web/index.html", "error": "web/notfound.html",
                      "css": "web/style.css", "js": "web/app.js", "json": "data/data.json",
                      "png": "web/icon.png"}
        self.pages = self.preload_pages()
        self.water_on = False
        self.water_off = False

    def preload_pages(self):
        pages = {}
        for name, file_name in self.files.items():
            if name == "png":
                with open(file_name, "rb") as f:
                    pages[name] = f.read()
            else:
                with open(file_name, "r") as f:
                    pages[name] = str(f.read())
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

        print(get_datetime(), "Server got request:", request)

        if "/water_on?" in request:
            self.water_on = True
            self.water_off = False
        elif "/water_off?" in request:
            self.water_off = True
            self.water_on = False

        html_requests = ["/", "//", "/index.html", "/water_on?", "/water_off?", "/set_thresholds?"]

        if request in html_requests:
            header = self.create_standard_header("text/html")
            response = self.create_html_response(REPLACEMENTS)
        elif "style.css" in request:
            header = self.create_standard_header("text/css")
            response = self.pages["css"]
        elif "app.js" in request:
            header = self.create_standard_header("application/javascript")
            response = self.pages["js"]
        elif "data.json" in request:
            header = self.create_standard_header("application/json")
            response = self.pages["json"]
        elif "icon.png" in request:
            header = self.create_standard_header("image/png")
            response = self.pages["png"]
        else:
            header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
            response = self.pages["error"]

        return header, response

    def create_html_response(self, replacements):
        response = self.pages["html"]
        for r in replacements:
            response = response.replace(r, str(replacements[r]))
        return response

    @staticmethod
    def create_standard_header(content_type):
        return f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nCache-Control: max-age=60\r\n\r\n"


async def update_file():
    """
    Writes last measurement along with timestamp to file
    """
    while True:
        datetime = get_datetime()
        print(datetime, "Data saved to file")
        entry = data.Entry(datetime, sensor.moisture, sensor.temp)
        data.append_entry(entry)

        with open("data/data.json", "r") as file:
            server.pages["json"] = str(file.read())

        await asyncio.sleep(1800)


async def update_fast():
    while True:
        sensor.update()
        valve.open() if LED_GRN.value() else valve.close()

        REPLACEMENTS["{temperature}"] = sensor.temp
        REPLACEMENTS["{moisture}"] = sensor.moisture
        REPLACEMENTS["{water_on}"] = valve.is_open
        REPLACEMENTS["{datetime}"] = get_time()
        REPLACEMENTS["{dry_threshold}"] = c.configs["DRY_LEVEL"]
        REPLACEMENTS["{wet_threshold}"] = c.configs["WET_LEVEL"]
        REPLACEMENTS["{is_morning}"] = is_morning()
        await asyncio.sleep(10)


async def set_leds():
    while True:
        LED_RED.value(sensor.dry)

        if server.water_on:
            LED_GRN.on()
            server.water_on = False
        elif server.water_off:
            LED_GRN.off()
            server.water_off = False
        else:
            if sensor.wet:
                LED_GRN.off()
            elif sensor.dry:
                LED_GRN.on()
            else:
                LED_GRN.value(is_morning())

        await asyncio.sleep(1)


def startup_blink():
    for n in range(3):
        LED_ONBOARD.off()
        time.sleep(0.2)
        LED_ONBOARD.on()
        time.sleep(0.2)


async def task_loop():
    loop = asyncio.get_event_loop()
    asyncio.create_task(asyncio.start_server(server.serve, server.host, server.port))
    asyncio.create_task(set_leds())
    asyncio.create_task(update_fast())
    asyncio.create_task(update_file())
    loop.run_forever()


if __name__ == "__main__":
    c = Config("config.json")
    wifi = WiFi(c.configs["WIFI_NAME"], c.configs["WIFI_PASS"], c.configs["STATIC_IP"])
    set_rtc()

    sensor = SoilSensor(PIN_SCL, PIN_SDA, c.configs["DRY_LEVEL"], c.configs["WET_LEVEL"],
                        c.configs["MIN_MOISTURE"], c.configs["MAX_MOISTURE"])
    valve = WaterValve(PIN_VALVE)
    data = DataFile(DATA_FILE)
    server = DataServer(wifi.ip)

    REPLACEMENTS = {}

    try:
        startup_blink()
        asyncio.run(task_loop())
    finally:
        asyncio.new_event_loop()
        machine.reset()
