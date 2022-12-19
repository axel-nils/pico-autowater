"""
Main program that automatically runs when Pico is powered
"""
from machine import Pin, Timer
from is_sensor import SoilSensor
from is_time import BackupTime
from is_data import DataDict


SCL_PIN = Pin(17)
SDA_PIN = Pin(16)
LED_GRN = Pin(11, Pin.OUT)
LED_RED = Pin(10, Pin.OUT)

DATA_FILE = "data/data.json"
TIME_FILE = "data/backup_time.txt"
DATA_DELAY = 3600 * 1000 # Once per hour
UPDATE_DELAY = 7 * 1000 # Once every 10 seconds


def data_tick(timer):
    """
    Writes last measurement along with timestamp to file
    """
    data.add(str(time), sensor.values())
    data.save()


def update_tick(timer):
    """
    Updates sensor measurements, backup time and led status
    """
    time.update()
    sensor.update()
    
    if sensor.mean_moisture() < 825:
        LED_RED.on()
    elif sensor.mean_moisture() > 850:
        LED_RED.off()
    
    LED_GRN.on() if sensor.moisture_series[0] == 0 else LED_GRN.off()  


if __name__ == "__main__":
    time: BackupTime = BackupTime(TIME_FILE)
    sensor: SoilSensor = SoilSensor(SCL_PIN, SDA_PIN)
    data: DataDict = DataDict(DATA_FILE)
    tim1 = Timer(period=DATA_DELAY, callback=data_tick)
    tim2 = Timer(period=UPDATE_DELAY, callback=update_tick)
    LED_GRN.off()
    LED_RED.off()
