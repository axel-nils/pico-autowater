"""
For plotting data
"""

from is_data import DataDict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_FILE = "data/data.json"

d = DataDict(DATA_FILE).data
keys = sorted(d.keys())
y = [d[key]["moisture"] for key in keys]
x = [pd.to_datetime(key) for key in keys]

plt.title("Moisture data")
plt.xlabel("date and time")
plt.ylabel("moisture level")

ax = plt.gca()
formatter = mdates.DateFormatter("%Y-%m-%d %H:%M")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)

plt.plot(x, y)
plt.grid()
plt.show()
