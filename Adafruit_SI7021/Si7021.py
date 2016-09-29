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

import logging
import math


# Default I2C address for device.
SI7021_I2CADDR_DEFAULT        = 0x40

## Commands.
SI7021_CMD_MEAS_RH_MSTR         = 0xE5  # Measure Relative Humidity, Hold Master Mode
SI7021_CMD_MEAS_RH_NOMSTR       = 0xF5  # Measure Relative Humidity, No Hold Master Mode
SI7021_CMD_MEAS_TEMP_MSTR       = 0xE3  # Measure Temperature, Hold Master Mode
SI7021_CMD_MEAS_TEMP_NOMSTR     = 0xF3  # Measure Temperature, No Hold Master Mode
SI7021_CMD_READ_RH_TEMP         = 0xE3  # Read Temperature Value from Previous RH Measurement
SI7021_CMD_RESET                = 0xFE  # Reset 
SI7021_CMD_WRITE_REG1           = 0xE6  # Write RH/T User Register 1
SI7021_CMD_READ_REG1            = 0xE7  # Read RH/T User Register 1
SI7021_CMD_WRITE_HEATER_REG     = 0x51  # Write Heater Control Register
SI7021_CMD_READ_HEATER_REG      = 0x11  # Read Heater Control Register
#SI7021_CMD_READ_ID_B1           = 0xFA, 0X0F # Read Electronic ID 1st Byte
#SI7021_CMD_READ_ID_B2           = 0xFC, 0xC9 # Read Electronic ID 2nd Byte
#SI7021_CMD_READ_FIRMWARE_REV    = 0x84, 0xB8 # Read Firmware Revision

## Configuration register values.
SI7021_REG1_CONFIG_MEAS_RES     = 0x81  # Measurement Resolution:
                                        # 00: RH 12b, Temp 14b
                                        # 01: RH  8b, Temp 12b
                                        # 10: RH 10b, Temp 13b
                                        # 11: RH 11b, Temp 11b
SI7021_REG1_CONFIG_VDDS         = 0x40  # VDD Status
                                        # 0: VDD OK, 1: VDD Low
SI7021_REG1_CONFIG_HTRE         = 0x04  # Heater Enabled
                                        # 1: Enabled, 0: Disabled
SI7021_REG2_CONFIG_HEATER       = 0x0F  # Heater Current Values
                                        # 0000 ~= 3.09 mA -> 1111 ~- 94.20 mA (non-linear)


class Si7021(object):
    """Class to represent an Adafruit SI7021 temperature and humidity measurement breakout board.
    """

    def __init__(self, address=SI7021_I2CADDR_DEFAULT, i2c=None, **kwargs):
        """Initialize Si7021 device on the specified I2C address and bus number.
        Address defaults to 0x40 and bus number defaults to the appropriate bus
        for the hardware."""
        self._logger = logging.getLogger('Adafruit_Si7021.Si7021')
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)

    
    def begin(self):
        """Start taking temperature measurements. Returns True if the device is 
        intialized, False otherwise."""
        ## Check manufacturer and device ID match expected values.
        #mid = self._device.readU16BE(MCP9808_REG_MANUF_ID)
        #did = self._device.readU16BE(MCP9808_REG_DEVICE_ID)
        #self._logger.debug('Read manufacturer ID: {0:04X}'.format(mid))
        #self._logger.debug('Read device ID: {0:04X}'.format(did))
        #return mid == 0x0054 and did == 0x0400
        reg1 = self._device.readU8(SI7021_CMD_READ_REG1)
        self._logger.debug('Register 1 raw value 0x%02X', reg1)
        return True

    def readRH(self):
        """Read Relative humidity and return its value in % RH."""
        # Send command to read RH
        rh = self._device.readU8(SI7021_CMD_MEAS_RH_NOMSTR);
        
        self._logger.debug('Raw relative humidity register value: 0x{0:04X}'.format(rh & 0xFFFF))
        # Scale and convert to a percentage value.
        rel_humid = 125.0 * rh / 65536.0 - 6.0
        return rel_humid

    def readTempC(self):
        """Read sensor and return its value in degrees celsius."""
        # Read temperature register value.
        t = self._device.readU16BE(SI7021_CMD_MEAS_TEMP_NOMSTR)
        self._logger.debug('Raw ambient temp register value: 0x{0:04X}'.format(t & 0xFFFF))
        # Scale and convert to signed value.
        temp = ( 175.72 * t ) / 65536.0 -46.85
        return temp
