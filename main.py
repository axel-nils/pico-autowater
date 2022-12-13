"""Main program that automatically runs when Pico is powered."""
from machine import Pin, Timer
from soil_sensor import SoilSensor
from backup_time import BackupTime


SCL_PIN = Pin(17)
SDA_PIN = Pin(16)
LED_GRN = Pin(10, Pin.OUT)
LED_RED = Pin(11, Pin.OUT)

DATA_FILE = "data.txt"
TIME_FILE = "backup_time.txt"
DATA_DELAY = 3600 * 1000 # Once per hour
UPDATE_DELAY = 10 * 1000 # Once every 10 seconds

def data_tick(timer):
    """Writes last moisture measurement along with timestamp to file"""
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(f"{sensor.moisture} {time}")


def update_tick(timer):
    """Updates sensor measurements, backup time and led status"""
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
