"""
For plotting data
"""

from is_data import DataDict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_FILE = "data/data.json"


def get_data():
    d = DataDict(DATA_FILE).data
    keys = sorted(d.keys())
    time = [pd.to_datetime(key) for key in keys]
    moisture = [d[key]["moisture"] for key in keys]
    return time, moisture


def set_labels():
    plt.title("Moisture data")
    plt.xlabel("date and time")
    plt.ylabel("moisture level")


def apply_formatting():
    ax = plt.gca()

    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    # formatter = mdates.DateFormatter("%Y-%m-%d %H:%M")
    formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_formatter(formatter)

    min_y, max_y = min(y), max(y)
    y_range = max_y - min_y
    plt.ylim(min_y - y_range, max_y + y_range)


if __name__ == "__main__":
    x, y = get_data()
    plt.plot(x, y)
    set_labels()
    apply_formatting()
    plt.grid()
    plt.show()

