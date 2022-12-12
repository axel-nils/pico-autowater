""" Module for reading sensor data from Adafruit STEMMA Soil Sensor """

from machine import I2C, Pin
import struct
from time import sleep

class SoilSensor:


    MS_ADDR = 0x36
    MS_TEMP_BASE = 0x00
    MS_TEMP_OFFSET = 0x04
    MS_TOUCH_BASE = 0x0F
    MS_TOUCH_OFFSET = 0x10


    def __init__(self, scl_pin: Pin, sda_pin: Pin, debug: bool=False):
        """Uses machine.Pin parameters to initialize I2C communication with sensor unit"""
        self.i2c: I2C = I2C(0, scl=scl_pin, sda=sda_pin)
        self.temp: int = self.update_moisture()
        self.moisture: int = self.update_moisture()

        if debug:
            devices = self.i2c.scan()
            if devices:
                for d in devices:
                    print(hex(d))


    def read_sensor(self, base, offset: int, nbytes: int) -> bytearray:
        """Helper method for reading data from adress in sensor memory"""
        temp = bytearray([base, offset])
        self.i2c.writeto(self.MS_ADDR, temp)
        sleep(0.005)
        buf = bytearray(nbytes)
        buf = self.i2c.readfrom_mem(self.MS_ADDR, offset, nbytes)
        return buf

    
    def update_temp(self) -> int:
        """Updates and returns the measured temperature"""
        buf = bytearray(self.read_sensor(self.MS_TEMP_BASE, self.MS_TEMP_OFFSET, 4))
        buf[0] = buf[0] & 0x3F
        t = 0.00001525878 * struct.unpack(">I", buf)[0]
        self.temp = t
        return t


    def update_moisture(self) -> int:
        """Updates and returns the measured moisture"""
        buf = self.read_sensor(self.MS_TOUCH_BASE, self.MS_TOUCH_OFFSET, 2)
        m = struct.unpack(">H", buf)[0]
        self.moisture = m
        return m


    def update(self):
        self.update_temp()
        self.update_moisture()


    def __str__(self):
        return f"Moisture reading: {self.moisture}. Temperature reading: {self.temp} °C."
