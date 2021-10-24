#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import adafruit_dht
import time
import board


def initialize():
    return adafruit_dht.DHT22(board.D4)


def get_temperature(dhtSensor, in_celsius=True, digits=3):
    while True:
        try:
            t = dhtSensor.temperature
            return round(t if in_celsius else (9.0 * t / 5) + 32.0, digits)
        except RuntimeError:
            pass


def get_humidity(dhtSensor, digits=3):
    while True:
        try:
            return round(dhtSensor.humidity, digits)
        except RuntimeError:
            pass


if __name__ == "__main__":
    dhtSensor = initialize()

    g = Gauge("temperature", "Temperature")
    h = Gauge("humidity", "Humidity")

    g.set_function(lambda: get_temperature(dhtSensor, False))
    h.set_function(lambda: get_humidity(dhtSensor))

    start_http_server(8001)
    while True:
        time.sleep(120)
