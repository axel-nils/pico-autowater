"""
For plotting data
"""

from is_data import DataDict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import EngFormatter

DATA_FILE = "data/example_data.json"
MIN_MOISTURE = 600


def normalize(values: list, min_from: int, max_from: int, min_to: int, max_to: int):
    return [min_to + (max_to - min_to) * ((value - min_from) / (max_from - min_from)) for value in values]


def get_data():
    d = DataDict(DATA_FILE).data
    keys = sorted(d.keys())

    time: list = [pd.to_datetime(key) for key in keys]
    raw_moisture = [d[key]["moisture"] for key in keys]
    moisture: list = normalize(raw_moisture, MIN_MOISTURE, max(raw_moisture), 0, 100)
    temperature: list = [d[key]["temp"] for key in keys]

    return time, moisture, temperature


def plot_moisture(ax, t, m):
    ax.set_title("Moisture data")
    ax.set_xlabel("Date")
    ax.set_ylabel("Soil moisture")

    ax.grid()
    ax.plot(t, m, '.-')

    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    xform = mdates.AutoDateFormatter(locator, defaultfmt="%Y-%m-%d %H:%M")
    yform = EngFormatter("%")
    ax.xaxis.set_major_formatter(xform), ax.yaxis.set_major_formatter(yform)


def plot_drying(ax, te, m, ti):
    ax.set_title("Drying")
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Change in moisture")

    dm = [m[n + 1] - m[n] for n in range(len(m) - 1)]
    dt = [(ti[n + 1] - ti[n]).seconds / 3600 for n in range(len(ti) - 1)]
    timecolor = [(d/(max(dt)), 0.1, 0.9) for d in dt]

    dmdt = [m / t for m, t in zip(dm, dt)]

    ax.grid()
    ax.scatter(te[0:-1], dmdt, s=m[0:-1], c=timecolor, alpha=0.5)

    xform = EngFormatter("°C")
    yform = EngFormatter("%/h")
    ax.xaxis.set_major_formatter(xform), ax.yaxis.set_major_formatter(yform)


if __name__ == "__main__":
    times, moistures, temps = get_data()

    fig, (ax1, ax2) = plt.subplots(2, 1)

    plot_moisture(ax1, times, moistures)
    plot_drying(ax2, temps, moistures, times)

    plt.show()

