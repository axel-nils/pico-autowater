"""
Module containing classes for writing and retrieving data
"""

import json


class DataDict:
    """
    Python dictionary using json format from local file
    """
    
    def __init__(self, dict_file: str, debug: bool = False) -> None:
        self.file_name = dict_file
        self.debug = debug
        self.data = dict()
        self.read()

    def read(self) -> None:
        """
        Try reading data from file. If any exception gets thrown, the data attribute remains unchanged.
        """

        with open(self.file_name, "r", encoding="utf-8") as file:
            content = file.read()
        self.data = json.loads(content)
        if self.debug:
            print(f"successfully read data from {self.file_name}")

    def add(self, key: str, value) -> None:
        """
        Add key-value pair to dictionary
        """
        self.data[key] = value

    def save(self) -> None:
        """
        Write dictionary to file
        """

        with open(self.file_name, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.data))
            if self.debug:
                print(f"successfully saved data to {self.file_name}")

    def __str__(self) -> str:
        return "\n".join([str(item) for item in self.data.items()])


if __name__ == "__main__":
    # Example usage: Combining data.json into example_data.json
    d = DataDict("data/data.json")
    d2 = DataDict("data/all_data.json")
    d2.data.update(d.data)
    d2.save()


    