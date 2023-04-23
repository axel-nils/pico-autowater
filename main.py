import uasyncio as asyncio
import gc

from devices import *
from utils import *

DATA_FILE = "data.json"
CONFIG_FILE = "config.json"

replacements = dict()


def startup_blink():
    for n in range(3):
        LED_ONBOARD.off()
        time.sleep(0.2)
        LED_ONBOARD.on()
        time.sleep(0.2)


async def gather_values():
    while True:
        sensor.update()
        replacements["{temperature}"] = sensor.temp
        replacements["{moisture}"] = sensor.moisture
        replacements["{water_on}"] = valve.is_open
        replacements["{datetime}"] = tu.datetime_str()[11:]
        replacements["{dry_threshold}"] = c.dry_level
        replacements["{wet_threshold}"] = c.wet_level
        server.system_status = replacements
        await asyncio.sleep(10)


async def handle_io():
    while True:
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
                LED_GRN.value(tu.is_morning())

        LED_RED.value(sensor.dry)
        valve.open() if LED_GRN.value() else valve.close()
        await asyncio.sleep(1)


async def log_data():
    while True:
        delay = 60 * (60 - tu.minute)
        await asyncio.sleep(delay)
        datetime = tu.datetime_str()
        entry = data.Entry(datetime, sensor.moisture, sensor.temp, valve.is_open)
        data.append_entry(entry)
        with open(DATA_FILE, "r") as file:
            server.pages["json"] = str(file.read())
        gc.collect()


async def keep_connection():
    while True:
        if not wifi.test_connection():
            wifi.attempt_connection()
        replacements["{weather}"] = WeatherApi().get()
        await asyncio.sleep(600)


async def main():
    startup_blink()
    asyncio.create_task(gather_values())
    asyncio.create_task(handle_io())
    asyncio.create_task(log_data())
    asyncio.create_task(server.run_server())
    asyncio.create_task(keep_connection())
    while True:
        await asyncio.sleep(tu.seconds_until_time(8, 30))
        LED_ONBOARD.off()
        from machine import WDT
        WDT(timeout=0)


if __name__ == "__main__":
    c = Config(CONFIG_FILE)
    data = DataFile(DATA_FILE)
    sensor = SoilSensor(PIN_SCL, PIN_SDA, c.dry_level, c.wet_level, c.min_moisture, c.max_moisture)
    valve = WaterValve(PIN_VALVE)
    wifi = WiFi(c.wifi_name, c.wifi_pass, c.static_ip)
    tu = TimeUtils()
    ws = WeatherApi()
    server = DataServer(wifi.ip)
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

    try:
        asyncio.run(main())
    finally:
        LED_ONBOARD.off()
