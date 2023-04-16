"""
Main program that automatically runs when Pico is powered
"""

import uasyncio as asyncio
import time
import gc
import machine

from devices import *
from utils import *

DATA_FILE = "data.json"
CONFIG_FILE = "config.json"

replacements = dict()


async def hourly_data_collection():
    """
    Writes last measurement along with timestamp to file
    """
    while True:
        delay = 60 * (60 - get_time()[1])
        await asyncio.sleep(delay)
        datetime = get_datetime_str()
        entry = data.Entry(datetime, sensor.moisture, sensor.temp, valve.is_open)
        data.append_entry(entry)
        with open(DATA_FILE, "r") as file:
            server.pages["json"] = str(file.read())
        gc.collect()


def get_replacements_values():
    replacements["{temperature}"] = sensor.temp
    replacements["{moisture}"] = sensor.moisture
    replacements["{water_on}"] = valve.is_open
    replacements["{datetime}"] = get_time_str()
    replacements["{dry_threshold}"] = c.dry_level
    replacements["{wet_threshold}"] = c.wet_level
    return replacements


async def read_sensor():
    while True:
        sensor.update()
        valve.open() if LED_GRN.value() else valve.close()
        server.system_status = get_replacements_values()
        await asyncio.sleep(10)


async def keep_connection():
    while True:
        replacements["{weather}"] = get_weather_str()
        if not wifi.test_connection():
            wifi.attempt_connection()
        await asyncio.sleep(600)


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


async def queue_restart():
    delay = 60 * (60 - get_time()[1])
    asyncio.sleep(900)
    machine.reset()


async def task_loop():
    loop = asyncio.get_event_loop()
    asyncio.create_task(server.run_server())
    asyncio.create_task(set_leds())
    asyncio.create_task(read_sensor())
    asyncio.create_task(hourly_data_collection())
    asyncio.create_task(keep_connection())
    loop.run_forever()


if __name__ == "__main__":
    c = Config(CONFIG_FILE)
    data = DataFile(DATA_FILE)

    sensor = SoilSensor(PIN_SCL, PIN_SDA, c.dry_level, c.wet_level, c.min_moisture, c.max_moisture)
    valve = WaterValve(PIN_VALVE)

    wifi = WiFi(c.wifi_name, c.wifi_pass, c.static_ip)
    set_rtc()
    server = DataServer(wifi.ip)
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

    try:
        startup_blink()
        asyncio.run(task_loop())
    finally:
        asyncio.new_event_loop()
        LED_ONBOARD.off()
