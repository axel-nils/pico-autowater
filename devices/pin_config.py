from machine import Pin

LED_GRN = Pin(11, Pin.OUT)
LED_RED = Pin(10, Pin.OUT)
LED_ONBOARD = Pin("LED", Pin.OUT)

PIN_SCL = Pin(17)
PIN_SDA = Pin(16)

PIN_VALVE = Pin(15, Pin.OUT)  # TODO: Check if this is correct
