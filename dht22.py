#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import adafruit_dht
import time
import board
import sys

dhtSensor = adafruit_dht.DHT22(board.D4)
g = Gauge('temperature', 'Temperature')
h = Gauge('humidity', 'Humidity')

def get_temperature():
    while True:
        try:
            return dhtSensor.temperature
        except RuntimeError:
            pass

def get_humidity():
    while True:
        try:
            return dhtSensor.humidity
        except RuntimeError:
            pass

g.set_function(lambda: get_temperature())
h.set_function(lambda: get_humidity())

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    for line in sys.stdin:
        pass
