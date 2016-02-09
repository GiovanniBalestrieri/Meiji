#!/usr/bin/python

import config
import smbus,time
import i2cutils as I2CUtils
from bmp085 import BMP085
from itg3200 import SensorITG3200

if __name__ == "__main__":
	config.init()
	shutdown = 0
	bus = smbus.SMBus(1)
	bmp085 = BMP085(bus,0x77,"BMP085")
	gyro = SensorITG3200(1,0x68)
	gyro.default_init()
	zeroX,zeroY,zeroZ = gyro.calibrate(1000,0.002)
	while not shutdown == 1: 
		input = raw_input("")
		if input == 'p':
			tempPress = bmp085.read_temperature_and_pressure()	
			gx,gy,gz = gyro.read_data_calib()
			print 'T\t%.2f\nP\t%.2f\nA\t%f' % (tempPress[0],tempPress[1],bmp085.readAltitude())
			print 'gx:\t%d\ngy:\t%d\ngz:\t%d' % (gx,gy,gz)
