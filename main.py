from machine import Pin, Timer
from soil_sensor import SoilSensor
from backup_time import BackupTime


SCL_PIN = Pin(17)
SDA_PIN = Pin(16)
LED_GRN = Pin(10, Pin.OUT)
LED_RED = Pin(11, Pin.OUT)

DATA_FILE = "data.txt"
TIME_FILE = "backup_time.txt"
DATA_DELAY = 3600 * 1000
UPDATE_DELAY = 1000


def data_tick(timer):
    with open(DATA_FILE, "a") as file:
        file.write(f"{sensor.moisture} {time}")


def update_tick(timer):
    time.update()
    sensor.update()
    if sensor.moisture < 825:
        LED_RED.on()
    if sensor.temp < 27:
        LED_GRN.on()


if __name__ == "__main__":

    time: BackupTime = BackupTime(TIME_FILE)
    sensor: SoilSensor = SoilSensor(SCL_PIN, SDA_PIN)
    tim1 = Timer(period=DATA_DELAY, callback=data_tick)
    tim2 = Timer(period=UPDATE_DELAY, callback=update_tick)
    LED_GRN.off()
    LED_RED.off()


    while True:
        pass
