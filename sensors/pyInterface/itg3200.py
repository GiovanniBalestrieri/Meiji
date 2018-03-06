#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# ITG3200 gyroscope class
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
from scipy.signal import medfilt
from collections import deque

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
        
        # Rolling buffers
        self.buf_len = 11
        self.filt_len = 3
        self.data_x = []
        self.data_y = []
        self.data_z = []
        self.alpha_lp = 0.99

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

    def read_data_calib(self,filt=False):
        """Read and return data tuple for x, y and z axis
        as signed 16-bit integers.
        """
		gx = i2cutils.i2c_read_word_signed(self.bus,self.addr, 0x1d)
		gy = i2cutils.i2c_read_word_signed(self.bus,self.addr, 0x1f)
		gz = i2cutils.i2c_read_word_unsigned(self.bus,self.addr, 0x21)
    
        ret_x = gx-self.zeroX
        ret_y = gy-self.zeroY

        # UnWrapp data TODO optimize it
        if gz < -sensor.zeroZ*0.9:
            print("Cr : " + str(gz) + " > " + str(gz+self.zeroZ))
            gz += sensor.zeroZ
            ret_z = gz
        else:
            ret_z = gz-self.zeroZ
        
        items_x = deque(self.data_x)
        items_y = deque(self.data_y)
        items_z = deque(self.data_z)
        
        #print("raw: " + str(self.data_z))
        #print("   : "+str(items_z)+"len " + str(len(items_z)))

        if len(items_x) >= self.buf_len:
            items_x.popleft()
            items_y.popleft()
            items_z.popleft()
        
        items_x.append(ret_x)
        items_y.append(ret_y)
        items_z.append(ret_z)
        
        self.data_x = list(items_x)
        self.data_y = list(items_y)
        self.data_z = list(items_z)

        if filt:
            #self.med_filter_data()
            self.low_pass((ret_x,ret_y,ret_z))

        #print("raw: A " + str(self.data_z))

        return (self.data_x[-1], self.data_y[-1], self.data_z[-1])

    def med_filter_data(self):
        # TODO make a copy of the data, compute the mean and ret val
        self.data_x = list(medfilt(self.data_x,self.filt_len))
        self.data_y = list(medfilt(self.data_y,self.filt_len))
        self.data_z = list(medfilt(self.data_z,self.filt_len))

    def low_pass(self, data):
        # X comp
        new_x = (1-self.alpha_lp) * self.data_x[-2] + self.alpha_lp * self.data_x[-1]
        self.data_x[-1] = new_x
        # Y comp
        new_y = (1-self.alpha_lp) * self.data_y[-2] + self.alpha_lp * self.data_y[-1]
        self.data_y[-1] = new_y
        # Z comp 
        new_z = (1-self.alpha_lp) * self.data_z[-2] + self.alpha_lp * self.data_z[-1]
        self.data_z[-1] = new_z

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
	        gx, gy, gz = sensor.read_data_calib(filt=True)
            
	        print gz
            sensor.save_data_csv(0,gz,gz-sensor.zeroZ)
        except:
            print("Skipping values")
		time.sleep(0.1)

