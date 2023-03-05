import urequests

TIME_API_URL = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm"


def get_datetime_json() -> dict:
    time_r = urequests.get(TIME_API_URL)
    data = time_r.json()
    time_r.close()
    return data


def get_datetime() -> str:
    data = get_datetime_json()
    return data["datetime"]


def get_time() -> str:
    data = get_datetime_json()
    return data["time"]


def get_date() -> str:
    data = get_datetime_json()
    return data["date"]
