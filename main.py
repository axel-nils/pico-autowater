"""
Main program that automatically runs when Pico is powered
"""

import uasyncio as asyncio

import time

from devices import *
from utils import Config, DataServer, DataFile, WiFi, get_datetime, get_time, set_rtc, is_morning

DATA_FILE = "data/data.json"


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


def get_replacements_values():
    replacements = dict()
    replacements["{temperature}"] = sensor.temp
    replacements["{moisture}"] = sensor.moisture
    replacements["{water_on}"] = valve.is_open
    replacements["{datetime}"] = get_time()
    replacements["{dry_threshold}"] = c.dry_level
    replacements["{wet_threshold}"] = c.wet_level
    replacements["{is_morning}"] = is_morning()
    return replacements


async def update_fast():
    while True:
        sensor.update()
        valve.open() if LED_GRN.value() else valve.close()
        server.replacements = get_replacements_values()
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
    asyncio.create_task(server.run_server())
    asyncio.create_task(set_leds())
    asyncio.create_task(update_fast())
    asyncio.create_task(update_file())
    loop.run_forever()


if __name__ == "__main__":
    c = Config("config.json")
    wifi = WiFi(c.wifi_name, c.wifi_pass, c.static_ip)
    set_rtc()

    sensor = SoilSensor(PIN_SCL, PIN_SDA, c.dry_level, c.wet_level, c.min_moisture, c.max_moisture)
    valve = WaterValve(PIN_VALVE)
    data = DataFile(DATA_FILE)
    server = DataServer(wifi.ip)

    try:
        startup_blink()
        asyncio.run(task_loop())
    finally:
        asyncio.new_event_loop()
        LED_ONBOARD.off()
