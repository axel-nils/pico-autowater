from machine import Pin, Timer, I2C
import struct
from time import sleep, localtime

# Constants 
MS_ADDR = 0x36
MS_TEMP_BASE = 0x00
MS_TEMP_OFFSET = 0x04
MS_TOUCH_BASE = 0x0F
MS_TOUCH_OFFSET = 0x10
DATA_FILENAME = "data.txt"
MEASUREMENT_DELAY = 60 * 1000

# Function definitions
def read_sensor(base, offset, nbytes):
    temp = bytearray([base, offset])
    i2c.writeto(MS_ADDR, temp)
    sleep(0.005)
    
    buf = bytearray(nbytes)
    buf = i2c.readfrom_mem(MS_ADDR, offset, nbytes)
    return buf


def get_temp():
    buf = bytearray(read_sensor(MS_TEMP_BASE, MS_TEMP_OFFSET, 4))
    buf[0] = buf[0] & 0x3F
    ret = struct.unpack(">I", buf)[0]
    return (0.00001525878 * ret)


def get_moisture():
    buf = read_sensor(MS_TOUCH_BASE, MS_TOUCH_OFFSET, 2)
    ret = struct.unpack(">H", buf)[0]
    return ret


def tick(timer):
    m = get_moisture()
    ledred.value(m < 925)
    c_m = int((m - 300) / 7)
    
    t = get_temp()
    ledgreen.value(t > 28)
    c_t = int(t - 5)
    write_value(m)
    print(f"Fuktighet: {c_m}%, Temp {c_t} C")


def write_value(x):
    file1 = open(DATA_FILENAME, "a")
    l = localtime()
    file1.write(f"{x} ({l[2]}/{l[1]}/{l[0]} {l[3]}:{l[4]})\n")
    file1.close()


# Setup
ledred = Pin(10, Pin.OUT)
ledgreen = Pin(11, Pin.OUT)

i2c = I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

tim = Timer()
tim.init(period=MEASUREMENT_DELAY, callback=tick)


# Program start

ledgreen.off()
ledred.off()


devices = i2c.scan()
if devices:
    for d in devices:
        print(hex(d))


# Main loop
while True:
    pass

