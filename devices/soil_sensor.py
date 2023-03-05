"""
Module containing class for reading sensor data from Adafruit STEMMA Soil Sensor
"""

from time import sleep
import struct
from machine import I2C, Pin


class SoilSensor:
    """
    Contains temp and moisure values pulled from sensor using I2C
    """
    
    MS_ADDR = 0x36
    MS_TEMP_BASE = 0x00
    MS_TEMP_OFFSET = 0x04
    MS_TOUCH_BASE = 0x0F
    MS_TOUCH_OFFSET = 0x10

    def __init__(self, scl_pin: Pin, sda_pin: Pin, dry_threshold: int, wet_threshold: int, debug: bool = False):
        """
        Uses machine.Pin parameters to initialize I2C communication with sensor unit
        """
        self.i2c: I2C = I2C(0, scl=scl_pin, sda=sda_pin)
        self.dry_threshold: int = dry_threshold
        self.wet_threshold: int = wet_threshold

        self.temp: int = self.update_moisture()
        self.moisture: int = self.update_moisture()
        self.moisture_series: list[int] = [0, 0, 0, 0, 0]

        if debug:
            devices = self.i2c.scan()
            if devices:
                for device in devices:
                    print(hex(device))

    def read_sensor(self, base, offset: int, nbytes: int) -> bytearray:
        """
        Helper method for reading data from adress in sensor memory
        """
        temp = bytearray([base, offset])
        self.i2c.writeto(self.MS_ADDR, temp)
        sleep(0.005)
        buf = bytearray(nbytes)
        buf = self.i2c.readfrom_mem(self.MS_ADDR, offset, nbytes)
        return buf

    def update_temp(self) -> int:
        """
        Updates and returns the measured temperature
        """
        buf = bytearray(self.read_sensor(self.MS_TEMP_BASE, self.MS_TEMP_OFFSET, 4))
        buf[0] = buf[0] & 0x3F
        temp = 0.00001525878 * struct.unpack(">I", buf)[0]
        self.temp = temp
        return temp

    def update_moisture(self) -> int:
        """
        Updates and returns the measured moisture
        """
        buf = self.read_sensor(self.MS_TOUCH_BASE, self.MS_TOUCH_OFFSET, 2)
        moisture = struct.unpack(">H", buf)[0]
        self.moisture = moisture
        return moisture

    def update_moisture_series(self) -> list[int]:
        """
        Updates moisture series
        """
        new_series = []
        for i, m in enumerate(self.moisture_series):
            if i == 0:
                continue
            new_series.append(m)
        new_series.append(self.moisture)
        self.moisture_series = new_series
        return new_series

    def update(self):
        """'
        Retrieves new values for both temp and moisture
        """
        self.update_temp()
        self.update_moisture()
        self.update_moisture_series()

    def values(self) -> dict:
        """
        Returns dict with sensor values
        """
        return {"moisture": self.mean_moisture(), "temp": self.temp}

    def mean_moisture(self) -> int:
        """
        Returns mean of last 5 moisture readings
        """
        return sum(self.moisture_series) // len(self.moisture_series)

    def dry(self) -> bool:
        return self.mean_moisture() < self.dry_threshold

    def wet(self) -> bool:
        return self.mean_moisture() > self.wet_threshold

    def __str__(self):
        return f"Moisture reading: {self.moisture}. Temperature reading: {self.temp} °C."
