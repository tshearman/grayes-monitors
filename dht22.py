#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import adafruit_dht
import time
import board
import sys

dhtSensor = adafruit_dht.DHT22(board.D4)
g = Gauge('temperature', 'Temperature')
h = Gauge('humidity', 'Humidity')

def get_temperature(in_celsius=True):
    while True:
        try:
            t = dhtSensor.temperature
            return t if in_celsius else (9.0 * t / 5) + 32.0
        except RuntimeError:
            pass

def get_humidity():
    while True:
        try:
            return dhtSensor.humidity
        except RuntimeError:
            pass

g.set_function(lambda: get_temperature(False))
h.set_function(lambda: get_humidity())

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        time.sleep(120)
