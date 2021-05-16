from setuptools import setup

setup(
    name='grayes-monitors',
    version='0.1',
    install_requires=[
        'prometheus-client>=0.10.1',
        'adafruit-circuitpython-dht==3.6.0',
    ]
    scripts=['dht22.py']
)
