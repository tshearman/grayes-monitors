#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import time
import board
import busio
import digitalio
import math


calibration_points = [[35.0, 16.11], [44.5, 20.78]]


def initialize():
    cs = digitalio.DigitalInOut(board.D2)
    cs.direction = digitalio.Direction.OUTPUT
    cs.value = True
    spi = busio.SPI(board.SCK, MISO=board.MISO)
    return spi, cs


def calibrated(r, points):
    m = (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])
    return m * (r - points[0][0]) + points[0][1]


def read_bytes(spi, cs):
    while not spi.try_lock():
        pass
    try:
        spi.configure(baudrate=5000000, phase=0, polarity=0)
        cs.value = False
        result = bytearray(4)
        spi.readinto(result)
        cs.value = True
    finally:
        spi.unlock()
    return result


def bytes_to_celsius(b):
    temp = b[0] << 8 | b[1]
    if temp & 0x0001:
        return float("NaN")
    temp >>= 2
    if temp & 0x2000:
        temp -= 16384
    return temp * 0.25


def average_over(fnc, t=5, dt=1):
    ts = [dt * i for i in range(int(t / dt + 1))]
    fs = 0.0
    n = 0.0
    for n in ts:
        time.sleep(n)
        f = fnc()
        if not math.isnan(f):
            n += 1.0
            fs += f
    return fs / n


def get_temperature(spi, cs, in_celsius=True):
    while True:
        try:
            read = lambda: bytes_to_celsius(read_bytes(spi, cs))
            t = calibrated(average_over(read), calibration_points)
            return t if in_celsius else (9.0 * t / 5) + 32.0
        except RuntimeError:
            pass


if __name__ == "__main__":
    spi, cs = initialize()

    g = Gauge("temperature", "Temperature")
    g.set_function(lambda: get_temperature(spi, cs, False))

    start_http_server(8002)
    while True:
        time.sleep(120)
