"""
Module containing valve functionality
"""

from machine import Pin


class WaterValve:
    def __init__(self, pin: Pin):
        self.pin = pin
        self.is_open = False

    def open(self):
        if not self.is_open:
            self.is_open = True
            self.pin.on()

    def close(self):
        if self.is_open:
            self.is_open = False
            self.pin.off()
