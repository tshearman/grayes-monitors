#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import time
import dht22.dht22 as dht22
import max6675.max6675 as max6675

if __name__ == "__main__":

    spi, cs = max6675.initialize()
    dht = dht22.initialize()

    g = Gauge("temperature", "Temperature")
    h = Gauge("humidity", "Humidity")
    i = Gauge("thermocouple", "Thermocouple")

    stored_temperature = dht22.get_temperature(dht, False)
    stored_humidity = dht22.get_humidity(dht)
    stored_thermocouple = max6675.get_temperature(spi, cs, False)

    g.set_function(lambda: stored_temperature)
    h.set_function(lambda: stored_humidity)
    i.set_function(lambda: stored_thermocouple)

    start_http_server(8000)
    while True:
        stored_temperature = dht22.get_temperature(dht, False)
        stored_humidity = dht22.get_humidity(dht)
        stored_thermocouple = max6675.get_temperature(spi, cs, False)
        print(f"Temperature: {stored_temperature}")
        print(f"Humidity: {stored_humidity}")
        print(f"Thermocouple: {stored_thermocouple}")
        time.sleep(20)
