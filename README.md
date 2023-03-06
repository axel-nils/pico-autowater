# RBPI Pico Irrigation System
This is a hobby project using a Raspberry Pi Pico W (with wireless capabilities) to automatically water some plants.
All code is written in MicroPython, see the [official documentation](https://docs.micropython.org/en/latest/rp2/quickref.html) for details.
The Pico hosts a website to show current status and statistics as well as allow for remote control of the watering.
## Current functionality
Collects timestamped moisture and temperature data at a regular frequency to display on webpage.
## Hardware used
* Raspberry Pi Pico
* Adafruit STEMMA Soil Sensor (capacitive, based on ATSAMD10 chip)
* Relay
* Solenoid Valve (1/2", NC, 12 V)
* Water pipe (3/4")
* Breadboard
* LEDs
* Cables and power supply
## Todo
* Fix server performance with random strings for requests (to prevent caching) and gzip (to reduce file sizes)
* Images and schematics showing the system
* Automated watering
* More advanced data analysis
