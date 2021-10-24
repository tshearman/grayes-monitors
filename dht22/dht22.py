#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import adafruit_dht
import time
import board


def initialize():
    return adafruit_dht.DHT22(board.D4)


def get_temperature(dhtSensor, in_celsius=True, digits=3, attempts=5):
    while attempts > 0:
        try:
            t = dhtSensor.temperature
            if t:
                return round(t if in_celsius else (9.0 * t / 5) + 32.0, digits)
            return get_temperature(dhtSensor, in_celsius, digits, attempts-1)
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

    d = {"temp": get_temperature(dhtSensor, False), "humidity": get_humidity(dhtSensor) }

    g.set_function(lambda: d["temp"])
    h.set_function(lambda: d["humidity"])

    start_http_server(8001)
    while True:
        time.sleep(10)
        d["temp"] = get_temperature(dhtSensor, False)
        d["humidity"] = get_humidity(dhtSensor)
