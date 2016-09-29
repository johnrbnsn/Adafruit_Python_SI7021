# The MIT License (MIT)
# Copyright (c) 2016 John Robinson
# Author: John Robinson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import Adafruit_SI7021.Si7021 as Si7021
import logging

# Start a log file
logging.basicConfig(filename="Si7021Example.log", level=logging.DEBUG)
logging.info("simpletest.py started")

# Default constructor will use the default I2C address (0x40) and pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
sensor = Si7021.Si7021()

# Optionally you can override the address and/or bus number:
#sensor = Si2107.Si2107(address=0x40, busnum=2)

# Initialize communication with the sensor.
sensor.begin()

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
    rel_humid = sensor.readRH()
    print('Relative Humidity: {0:3F} %'.format(rel_humid))
    time.sleep(1.0)
