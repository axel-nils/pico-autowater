"""
Module containing valve functionality
"""

from machine import Pin


class WaterValve:
    def __init__(self, pin: Pin, open_time: int = 10):
        self.pin = pin
        self.opened = False

    def open(self):
        if not self.opened:
            self.opened = True
            self.pin.on()

    def close(self):
        if self.opened:
            self.opened = False
            self.pin.off()
