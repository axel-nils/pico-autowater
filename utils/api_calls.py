import urequests as requests
from machine import RTC
import time


class TimeUtils:
    time_url = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"

    @staticmethod
    def set_rtc():
        rtc = RTC()
        r = requests.get(TimeUtils.time_url)
        dt = r.json()
        r.close()
        dtt = dt["year"], dt["month"], dt["day"], dt["dayOfWeek"], dt["hour"], dt["minute"], dt["seconds"], 0
        rtc.datetime(dtt)
        print("RTC set to", TimeUtils.datetime_str())

    @staticmethod
    def minute():
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
