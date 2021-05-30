#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import time
import dht22.dht22 as dht22
import max6675.max6675 as max6675

if __name__ == "__main__":

    time.sleep(5)

    dht = dht22.initialize()

    g = Gauge("temperature", "Temperature")
    h = Gauge("humidity", "Humidity")
    i = Gauge("thermocouple", "Thermocouple")

    data = {
        "temp": dht22.get_temperature(dht, False),
        "humdity": dht22.get_humidity(dht),
    }
    print(data)
    time.sleep(5)

    g.set_function(lambda: dht22.get_temperature(dht, False))
    h.set_function(lambda: dht22.get_humidity(dht))
    i.set_function(lambda: data["thermo"])

    spi, cs = max6675.initialize()
    data = {"thermo": max6675.get_temperature(spi, cs, False)}
    print(data)
    i.set_function(lambda: data["thermo"])

    start_http_server(8000)
    while True:
        data["thermo"] = max6675.get_temperature(spi, cs, False)
        time.sleep(20)
