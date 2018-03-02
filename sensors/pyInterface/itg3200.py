#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# ITG3200 gyroscope control class
#
# Copyright 2013 Michal Belica <devel@beli.sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import smbus,time, i2cutils, csv

def int_sw_swap(x):
    """Interpret integer as signed word with bytes swapped"""
	xl = x & 0xff
	xh = x >> 8
	xx = (xl << 8) + xh
    return xx - 0xffff if xx > 0x7fff else xx

class SensorITG3200(object):
    """ITG3200 digital gyroscope control class.
    Supports data polling at the moment.
    """
    def __init__(self, bus_nr, addr):
       	""" Sensor class constructor
        Params:
            bus_nr .. I2C bus number
            addr   .. ITG3200 device address
        """
        self.bus = smbus.SMBus(bus_nr)
        self.zeroX = 20
        self.zeroY = -4726
        self.zeroZ = 23635
        self.addr = addr
        
        self.file = open("data.csv","wba")
        self.writer = csv.writer(self.file,delimiter=',')

    def sample_rate(self, lpf, div):
        """Set internal sample rate, low pass filter frequency.
        Sets device parameters DLPF_CFG and SMPLRT_DIV.
        Also sets FS_SEL to 0x03 which is required to initialize the device.
        Params:
            lpf .. (code from the list)
              code   LPF  sample rate
                0 256Hz  8kHz
                 1 188Hz  1kHz
                 2  98Hz  1kHz
                 3  42Hz  1kHz
                 4  20Hz  1kHz
                 5  10Hz  1kHz
                 6   5Hz  1kHz
            div .. internal sample rate divider (SMPLRT_DIV will be set to div-1)
        """
        if not (lpf >= 0 and lpf <= 0x6):
            raise ValueError("Invalid low pass filter code (0-6).")
        if not (div >= 0 and div <= 0xff):
            raise ValueError("Invalid sample rate divider (0-255).")
        self.bus.write_byte_data(self.addr, 0x15, div-1)
        self.bus.write_byte_data(self.addr, 0x16, 0x18 | lpf)

	def calibrate(self,samples,delay):
		(sumX,sumY,sumZ) = (0,0,0)
		for i in range(1,samples):	
		 	(gxT,gyT,gzT) = self.read_data_calib()
			sumX = sumX + gxT
			sumY = sumY + gyT
			sumZ = sumZ + gzT
			time.sleep(delay)
		(self.zeroX,self.zeroY,self.zeroZ) = (sumX/samples,sumY/samples,sumZ/samples)
		print "Gyro calibration ... [Ok]"

		return (self.zeroX,self.zeroY,self.zeroZ)
		
    def default_init(self):
        """Initialization with default values:
        8kHz internal sample rate, 256Hz low pass filter, sample rate divider 8.
        """
        self.sample_rate(1, 8)

    def read_data_calib(self):
        """Read and return data tuple for x, y and z axis
        as signed 16-bit integers.
        """
		gx = int_sw_swap(self.bus.read_word_data(self.addr, 0x1d))
		gy = int_sw_swap(self.bus.read_word_data(self.addr, 0x1f))
		gz = i2cutils.i2c_read_word_signed(self.bus,self.addr, 0x21)
		#gz = self.bus.read_word_data(self.addr, 0x21)

        return (gx-self.zeroX, gy-self.zeroY, gz-self.zeroZ)

    def save_data_csv(self,val1,val2,val3):
        data = ['g',val1,val2,val3,'z']
        self.writer.writerow(data)

if __name__ == '__main__':
    import time
    sensor = SensorITG3200(1, 0x68) # update your bus number & add
    sensor.default_init()
    time.sleep(0.1)

	#zeroX,zeroY,zeroZ = (0,0,0)
    print("Calibrating gyroscope ...")
	#zeroX,zeroY,zeroZ = sensor.calibrate(4000,0.002);
	#print "Bias: x " ,zeroX, " y ", zeroY, " z ", zeroZ
    while True:
        try:
	        gx, gy, gz = sensor.read_data_calib()
            # UnWrapp data TODO optimize it
            if gz<-sensor.zeroZ*0.9:
                gz += sensor.zeroZ
	        print gz, gz - sensor.zeroZ
            sensor.save_data_csv(0,gz,gz-sensor.zeroZ)
        except:
            print("Skipping values")
		time.sleep(0.1)

