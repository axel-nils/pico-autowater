"""
Module containing valve functionality
"""

from machine import Pin


class WaterValve:
    def __init__(self, pin: Pin):
        self.pin = pin

    def open(self):
        self.pin.on()

    def close(self):
        self.pin.off()

    @property
    def is_open(self):
        return bool(self.pin.value())
