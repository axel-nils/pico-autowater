import urequests
from machine import RTC
import time

TIME_API_URL = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"


def get_datetime_json() -> dict:
    time_r = urequests.get(TIME_API_URL)
    data = time_r.json()
    time_r.close()
    return data


def get_datetime_str() -> str:
    """
    Returns formatted datetime string with minute precision
    """
    dtt = time.localtime()
    date_str = f"{dtt[0]}-{dtt[1]:02d}-{dtt[2]:02d}"
    time_str = f"{dtt[3]:02d}:{dtt[4]:02d}"
    return f"{date_str}T{time_str}"


def get_time_str() -> str:
    time_tuple = time.localtime()
    return f"{time_tuple[3]:02d}:{time_tuple[4]:02d}:{time_tuple[5]:02d}"


def get_time() -> tuple:
    return time.localtime()[3:6]


def get_date() -> str:
    data = get_datetime_json()
    return data["date"]


def set_rtc() -> None:
    rtc = RTC()
    dt = get_datetime_json()
    dtt = dt["year"], dt["month"], dt["day"], dt["dayOfWeek"], dt["hour"], dt["minute"], dt["seconds"], 0
    rtc.datetime(dtt)
    print("RTC set to", get_datetime_str())


def is_morning() -> bool:
    time_tuple = time.localtime()
    return 6 <= int(time_tuple[3]) < 11

