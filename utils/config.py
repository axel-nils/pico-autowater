import json


class Config:
    def __init__(self, path):
        self.path = path
        self.configs = {"MAX_MOISTURE": None,
                        "MIN_MOISTURE": None,
                        "WET_LEVEL": None,
                        "DRY_LEVEL": None,

                        "WIFI_NAME": None,
                        "WIFI_PASS": None,
                        "STATIC_IP": None}
        try:
            with open(self.path, "r") as f:
                json_object: dict = json.load(f)
                for key in self.configs.keys():
                    if key in json_object:
                        self.configs[key] = json_object[key]
        except:
            print(f"Failed reading \"{path}\", please enter desired values in generated file")
            self.save()

    def update(self, key, value):
        self.configs[key] = value
        self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.configs, f, indent=2)


if __name__ == "__main__":
    c = Config("../config.json")
    print(c.configs)
