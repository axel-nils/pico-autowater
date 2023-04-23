import urequests as requests
from machine import RTC
import time


class WeatherApi:
    icons_url = "https://api.met.no/weatherapi/weathericon/2.0/legends"
    headers = {"User-Agent": "pico-autowater https://github.com/axel-nils/pico-autowater"}

    def __init__(self):
        self.weather_url = f"https://api.met.no/weatherapi/nowcast/2.0/complete?lat=57.4&lon=12.0"
        r = requests.get(WeatherApi.icons_url, headers=WeatherApi.headers)
        self.descriptions = r.json()
        r.close()

    def get(self) -> str:
        """Gives string with temperature and description of current weather"""
        r = requests.get(self.weather_url, headers=WeatherApi.headers)
        data = r.json()["properties"]["timeseries"][0]["data"]
        r.close()
        temp = int(data["instant"]["details"]["air_temperature"])
        code = data["next_1_hours"]["summary"]["symbol_code"]
        desc = self.descriptions[code.split("_")[0]]["desc_nb"].lower()  # "desc_en" for english
        return f"Utomhus är det {temp} °C och {desc}."


class TimeUtils:
    time_url = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"

    def __init__(self):
        rtc = RTC()
        r = requests.get(TimeUtils.time_url)
        dt = r.json()
        r.close()
        dtt = dt["year"], dt["month"], dt["day"], dt["dayOfWeek"], dt["hour"], dt["minute"], dt["seconds"], 0
        rtc.datetime(dtt)
        print("RTC set to", TimeUtils.datetime_str())

    @property
    def minute(self):
        return time.localtime()[4]

    @staticmethod
    def datetime_str() -> str:
        """
        Returns string of format: YYYY-MM-DDThh:mm
        """
        dtt = time.localtime()
        date_str = f"{dtt[0]}-{dtt[1]:02d}-{dtt[2]:02d}"
        time_str = f"{dtt[3]:02d}:{dtt[4]:02d}"
        return f"{date_str}T{time_str}"

    @staticmethod
    def is_morning() -> bool:
        time_tuple = time.localtime()
        return 6 <= int(time_tuple[3]) < 11

    @staticmethod
    def seconds_until_time(hour: int, minute=0, second=0) -> int:
        dtt = time.localtime()
        return (3600 * hour + 60 * minute + second - (3600 * dtt[3] + 60 * dtt[4] + dtt[5])) % 86400

