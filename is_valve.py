"""
Module containing valve functionality
"""

from machine import Pin, Timer

class WaterValve:
    def __init__(self, pin: int, open_time: int = 10):
        self.pin = Pin(pin)
        self.opened = False
        self.open_time = open_time
        self.timer = Timer()

    def open(self):
        self.opened = True
        self.pin.on()
        self.timer.init(mode=Timer.ONE_SHOT, period=1000*self.open_time, callback=autoclose)
    
    def close(self):
        self.opened = False
        self.pin.off()
        self.timer.deinit()

def autoclose(timer):
    WaterValve.close()
