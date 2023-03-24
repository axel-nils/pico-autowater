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

    def __init__(self, scl_pin: Pin, sda_pin: Pin, dry_threshold, wet_threshold, min_moisture, max_moisture):
        """
        Uses machine.Pin parameters to initialize I2C communication with sensor unit
        Dry and wet thresholds should be set to values between 0 and 100
        """
        self.i2c: I2C = I2C(0, scl=scl_pin, sda=sda_pin)

        self.temp: int = 0
        self.raw_moisture: int = 0
        self.moisture: int = 0
        self.moisture_series: list[int] = []

        self.dry_threshold: int = dry_threshold
        self.wet_threshold: int = wet_threshold
        self.min_moisture = min_moisture
        self.max_moisture = max_moisture
        self.dry: bool = False
        self.wet: bool = False

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

    def update_temp(self):
        """
        Updates and returns the measured temperature
        """
        buf = bytearray(self.read_sensor(self.MS_TEMP_BASE, self.MS_TEMP_OFFSET, 4))
        buf[0] = buf[0] & 0x3F
        temp = int(0.00001525878 * struct.unpack(">I", buf)[0])
        self.temp = temp

    def update_moisture(self):
        """
        Updates the measured moisture
        """
        buf = self.read_sensor(self.MS_TOUCH_BASE, self.MS_TOUCH_OFFSET, 2)
        self.raw_moisture = struct.unpack(">H", buf)[0]

        if len(self.moisture_series) >= 5:
            self.moisture_series.pop(0)
        self.moisture_series.append(self.raw_moisture)

        mean = sum(self.moisture_series) // len(self.moisture_series)
        self.moisture = int(100 * (mean - self.min_moisture) / (self.max_moisture - self.min_moisture))

    def update(self):
        """'
        Retrieves new values for both temp and moisture
        """
        self.update_temp()
        self.update_moisture()
        self.wet = self.moisture > self.wet_threshold
        self.dry = self.moisture < self.dry_threshold

    def values(self) -> tuple:
        """
        Returns tuple with moisture and temp values
        """
        return self.moisture, self.temp

    def __str__(self):
        return f"moisture: {self.moisture}%, temperature: {self.temp} °C."


if __name__ == "__main__":
    """
    Run this. Set min and max moisture constants to match totally dry and wet soil.
    """
    from pin_config import PIN_SCL, PIN_SDA
    i2c = I2C(0, scl=PIN_SCL, sda=PIN_SDA)

    devices = i2c.scan()
    if devices:
        for device in devices:
            print(hex(device))

    sensor = SoilSensor(PIN_SCL, PIN_SDA, 100, 500, 0, 1000)
    while True:
        sensor.update()
        print(sensor.raw_moisture, sensor.temp)
        sleep(1)
