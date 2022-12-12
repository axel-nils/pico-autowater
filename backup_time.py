""" Module for keeping track of time after losing power and internet using local file """

from machine import RTC

class BackupTime:

    def __init__(self, time_file: str):
        self.rtc = RTC()
        self.time_file = time_file
        self.update_time()


    def get_times(self):
        self.time = self.rtc.datetime()
        self.saved_time = self.read_saved_time()


    def read_saved_time(self):
        with open(self.time_file, "r") as file:
            time = file.readline()
        return eval(time)


    def save_time(self):
        with open(self.time_file, "w") as file:
            file.write(str(self.time))
        self.saved_time = self.read_saved_time()


    def update(self):
        self.get_times()
        if self.behind():
            self.rtc.datetime(self.saved_time)
            self.time = self.rtc.datetime()
        else:
            self.save_time()


    def behind(self) -> bool:
        a: tuple = self.time
        s: tuple = self.saved_time
        return self.list_behind(a, s)


    def list_behind(self, a: tuple, s: tuple) -> bool:
        if len(a) == 0:
            return False
        elif a[0] < s[0]:
            return True
        elif a[0] > s[0]:
            return False
        else:
            return self.list_behind(a[1:], s[1:])


    def __str__(self):
        date = str(self.time[0:3]).replace(",","/").replace(" ", "")
        time = str(self.time[4:7]).replace(",",":").replace(" ", "")
        return f"{date} {time}"
