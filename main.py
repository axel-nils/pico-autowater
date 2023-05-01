import uasyncio as asyncio
import gc

from devices import *
from utils import *

DATA_FILE = "data.json"
CONFIG_FILE = "config.json"


class SystemStatus:
    def __init__(self):
        self.datetime = tu.datetime_str()[11:]
        self.moisture = sensor.moisture
        self.temperature = sensor.temp
        self.valve_open = valve.is_open
        self.water_setting = server.water_setting
        self.dry_threshold = c.dry_level
        self.wet_threshold = c.wet_level
        self._website_data = dict()

    def update(self):
        self.datetime = tu.datetime_str()[11:]
        sensor.update()
        self.moisture = sensor.moisture
        self.temperature = sensor.temp
        self.valve_open = valve.is_open
        self.water_setting = server.water_setting

    @property
    def website_dict(self):
        self._website_data["{temperature}"] = self.temperature
        self._website_data["{moisture}"] = self.moisture
        self._website_data["{valve_open}"] = "öppen" if self.valve_open else "stängd"
        self._website_data["{water_setting}"] = WaterSettings.to_str(self.water_setting)
        self._website_data["{datetime}"] = self.datetime
        self._website_data["{dry_threshold}"] = self.dry_threshold
        self._website_data["{wet_threshold}"] = self.wet_threshold
        return self._website_data


def startup_blink():
    for n in range(3):
        LED_ONBOARD.off()
        time.sleep(0.2)
        LED_ONBOARD.on()
        time.sleep(0.2)


async def gather_values():
    while True:
        system.update()
        server.system_status = system.website_dict
        await asyncio.sleep(10)


async def handle_io():
    while True:
        if server.water_setting == WaterSettings.auto:
            if sensor.wet:
                valve.close()
            elif sensor.dry:
                valve.open()
            else:
                valve.open() if tu.is_morning() else valve.close()
        elif server.water_setting == WaterSettings.on:
            valve.open()
        elif server.water_setting == WaterSettings.off:
            valve.close()

        LED_RED.value(sensor.dry)
        LED_GRN.value(valve.is_open)
        await asyncio.sleep(1)


async def log_data():
    while True:
        delay = 60 * (60 - tu.minute)
        await asyncio.sleep(delay)
        datetime = tu.datetime_str()
        entry = data.Entry(datetime, sensor.moisture,
                           sensor.temp, valve.is_open)
        data.append_entry(entry)
        with open(DATA_FILE, "r") as file:
            server.pages["json"] = str(file.read())
        gc.collect()
        print("Data logged at ", datetime)


async def keep_connection():
    while True:
        if wifi.test_connection():
            print("WiFi ok")
        else:
            wifi.attempt_connection()
        await asyncio.sleep(600)


async def main():
    startup_blink()
    asyncio.create_task(gather_values())
    asyncio.create_task(handle_io())
    asyncio.create_task(log_data())
    asyncio.create_task(server.run_server())
    asyncio.create_task(keep_connection())
    while True:
        delay = tu.seconds_until_time(8, 30)
        print("Restarting in ", tu.seconds_until_time(8, 30))
        await asyncio.sleep(delay)
        shutdown()


def shutdown():
    from machine import WDT
    LED_ONBOARD.off()
    LED_RED.off()
    LED_GRN.off()
    WDT(timeout=0)


if __name__ == "__main__":
    c = Config(CONFIG_FILE)
    data = DataFile(DATA_FILE)
    sensor = SoilSensor(PIN_SCL, PIN_SDA, c.dry_level,
                        c.wet_level, c.min_moisture, c.max_moisture)
    valve = WaterValve(PIN_VALVE)
    wifi = WiFi(c.wifi_name, c.wifi_pass, c.static_ip)
    tu = TimeUtils()
    server = DataServer(wifi.ip)
    system = SystemStatus()

    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

    try:
        asyncio.run(main())
    finally:
        shutdown()
