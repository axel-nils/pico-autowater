import urequests
from machine import RTC
import time

TIME_API_URL = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"


def get_datetime_json() -> dict:
    time_r = urequests.get(TIME_API_URL)
    data = time_r.json()
    time_r.close()
    return data


def get_datetime() -> str:
    data = get_datetime_json()
    return data["dateTime"]


def get_time() -> str:
    return str(time.time())


def get_date() -> str:
    data = get_datetime_json()
    return data["date"]


def set_rtc() -> None:
    rtc = RTC()
    dt = get_datetime_json()
    dtt = dt["year"], dt["month"], dt["day"], dt["dayOfWeek"], dt["hour"], dt["minute"], dt["seconds"], 0
    rtc.datetime(dtt)
