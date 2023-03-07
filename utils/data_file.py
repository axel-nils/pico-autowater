"""
Module containing classes for writing and retrieving data
"""

import json
from collections import namedtuple


class DataFile:
    Entry = namedtuple("Entry", ["d", "m", "t"])  # For datetime, moisture and temperature
    template_json = {
        "dataKeys": ["d", "m", "t"],
        "data": []
    }

    def __init__(self, filename):
        self.filename = filename
        self.json = self.get_json()

    def save_json(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.json, f, separators=(',', ':'), indent=0)

    def get_json(self) -> dict:
        try:
            with open(self.filename, "r") as f:
                json_object = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            json_object = DataFile.template_json
            print(f"Failed reading {self.filename}")
        return json_object

    def append_entry(self, entry: Entry) -> None:
        data: list = self.data()
        data.append(entry._asdict())
        self.save_json()

    def entries(self) -> int:
        return len(self.data())

    def data(self):
        return self.json["data"]


if __name__ == "__main__":
    """
    Example usage
    """
    import random
    datafile = DataFile("../data/test_data.json")
    print(datafile.data())
    for i in range(10, 23):
        dt_str = "2023-03-07T" + str(i) + ":41:43.0191136"
        m = random.randint(600, 1000)
        t = random.randint(16, 23)
        e = datafile.Entry(dt_str, m, t)
        print(e)
        datafile.append_entry(e)

