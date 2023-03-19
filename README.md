# pico-autowater
This is a hobby project using a Raspberry Pi Pico W (with wireless capabilities) to automatically water some plants.
All code is written in MicroPython, see the [official documentation](https://docs.micropython.org/en/latest/rp2/quickref.html) for details.
The Pico hosts a website to show current status and statistics as well as allow for remote control of the watering.
## Current functionality
* Collects moisture and temperature data
* Hosts a website to show current status and statistics
## Hardware used
* Raspberry Pi Pico W
* Adafruit STEMMA Soil Sensor (capacitive, based on ATSAMD10 chip)
* Relay module (3.3 V, with protective diode)
* Solenoid Valve (12 V, 3/4", NC)
* Water pipe (3/4")
* Breadboard
* LEDs
* Cables and power supply
## Todo
* Images and schematics showing the system
* More advanced data analysis
