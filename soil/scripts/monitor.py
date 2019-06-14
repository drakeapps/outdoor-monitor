#!/usr/bin/env python3

import time
import os


from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw

from influxdb import InfluxDBClient

i2c_bus = busio.I2C(SCL, SDA)

ss = Seesaw(i2c_bus, addr=0x36)

remote_influx_client = InfluxDBClient('192.168.1.16', 8086, database='outdoor-%s' % (os.environ.get('BALENA_DEVICE_NAME_AT_INIT')))

remote_influx_client.create_database('outdoor-%s' % (os.environ.get('BALENA_DEVICE_NAME_AT_INIT')))


while True:
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()

    measurement = [
        {
            'measurement': 'soil',
            'fields': {
				'temp': temp,
				'moisture': touch
			}
        }
    ]
    remote_influx_client.write_points(measurement)


    print("temp: " + str(temp) + "  moisture: " + str(touch))
    time.sleep(5)