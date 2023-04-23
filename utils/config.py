import json


class Config:
    def __init__(self, path):
        self.path = path
        self._configs = {"MAX_MOISTURE": None,
                         "MIN_MOISTURE": None,
                         "WET_LEVEL": None,
                         "DRY_LEVEL": None,

                         "WIFI_NAME": None,
                         "WIFI_PASS": None,
                         "STATIC_IP": None}
        try:
            with open(self.path, "r") as f:
                json_object: dict = json.load(f)
                for key in self._configs.keys():
                    if key in json_object:
                        self._configs[key] = json_object[key]
        except:
            print(
                f"Failed reading \"{path}\", please enter desired values in generated file")
            self.save()

    def update(self, key, value):
        self._configs[key] = value
        self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self._configs, f, indent=2)

    @property
    def max_moisture(self) -> str:
        return self._configs["MAX_MOISTURE"]

    @property
    def min_moisture(self) -> str:
        return self._configs["MIN_MOISTURE"]

    @property
    def wet_level(self) -> str:
        return self._configs["WET_LEVEL"]

    @property
    def dry_level(self) -> str:
        return self._configs["DRY_LEVEL"]

    @property
    def wifi_name(self) -> str:
        return self._configs["WIFI_NAME"]

    @property
    def wifi_pass(self) -> str:
        return self._configs["WIFI_PASS"]

    @property
    def static_ip(self) -> str:
        return self._configs["STATIC_IP"]


if __name__ == "__main__":
    c = Config("../config.json")
    print(c._configs)
