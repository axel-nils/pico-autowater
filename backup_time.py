"""Module for keeping track of time after losing power and internet using local file"""

from machine import RTC

class BackupTime:
    """Contains time value that is kept current by, when needed, restoring backup saved in file"""

    def __init__(self, time_file: str):
        self.rtc = RTC()
        self.time_file = time_file
        self.time = None
        self.saved_time = None
        self.update()


    def get_times(self):
        """Updates class member values time and saved_time"""
        self.time = self.rtc.datetime()
        self.saved_time = self.read_saved_time()


    def read_saved_time(self):
        """Returns value of time tuple saved in backup file"""
        with open(self.time_file, "r", encoding="utf-8") as file:
            time = file.readline()
        return tuple(time)


    def save_time(self):
        """Writes current value of time to backup file"""
        with open(self.time_file, "w", encoding="utf-8") as file:
            file.write(str(self.time))
        self.saved_time = self.read_saved_time()


    def update(self):
        """Updates all time values, including RTC datetime, to most accurate"""
        self.get_times()
        if self.behind():
            self.rtc.datetime(self.saved_time)
            self.time = self.rtc.datetime()
        else:
            self.save_time()


    def behind(self) -> bool:
        """Compares time tuples, returns true if current time is behind saved time"""
        current: tuple = self.time
        saved: tuple = self.saved_time
        return self.list_behind(current, saved)


    def list_behind(self, current: tuple, saved: tuple) -> bool:
        """Compares values in a tuple one by one"""
        if len(current) == 0:
            return False
        if current[0] < saved[0]:
            return True
        if current[0] > saved[0]:
            return False
        return self.list_behind(current[1:], saved[1:])


    def __str__(self):
        date = str(self.time[0:3]).replace(",","/").replace(" ", "")
        time = str(self.time[4:7]).replace(",",":").replace(" ", "")
        return f"{date} {time}"
