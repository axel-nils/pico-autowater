# RBPI Pico Irrigation System
This is a hobby project using a Raspberry Pi Pico to automatically water some plants.
All code is written in MicroPython, see the [official documentation](https://docs.micropython.org/en/latest/rp2/quickref.html) for details.
## Current functionality
Collects timestamped moisture and temperature data at a regular frequency, and stores it conveniently in a JSON-file.
## Hardware used
* Raspberry Pi Pico
* Adafruit STEMMA Soil Sensor (capacitive, based on ATSAMD10 chip)
* Solenoid Valve (1/2", NC, 12 V)
* Relay (12 V)
* Breadboard
* LEDs
* Cables
## Todo
* Basic valve operation
* Images and schematics showing the system
* Watering in the morning
* More advanced data analysis
