"""
Module containing classes for writing and retrieving data
"""

import json
from collections import namedtuple


class DataFile:
    Entry = namedtuple(
        "Entry", ["datetime", "moisture", "temperature", "watering"])
    template_json = {
        "data_columns": ["datetime", "moisture", "temperature", "watering"],
        "data": []
    }

    def __init__(self, filename):
        self.filename = filename
        self.json = self.get_json()
        self.save_json()

    def save_json(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.json, f, separators=(',', ':'))

    def get_json(self) -> dict:
        try:
            with open(self.filename, "r") as f:
                json_object = json.load(f)
        except OSError as e:
            json_object = DataFile.template_json
            print(e)
        return json_object

    def append_entry(self, entry: Entry) -> None:
        self.data.append([value for value in entry])
        while len(self.data) > 168:
            self.data.pop(0)
        self.save_json()

    @property
    def data(self):
        return self.json["data"]


if __name__ == "__main__":
    """
    Example usage
    """
    import random
    datafile = DataFile("../data/test2_data.json")
    print(datafile.data())
    m = 50
    t = 18
    for i in range(10, 23):
        dt_str = "2023-03-07T" + str(i) + ":41:43.0191136"
        m += random.randint(-10, 10)
        t += random.randint(-2, 2)
        e = datafile.Entry(dt_str, m, t)
        print([value for value in e])
        datafile.append_entry(e)
