#!/usr/bin/python

import config
import smbus,time
import i2cutils as I2CUtils
from bmp085 import BMP085
from itg3200 import SensorITG3200
from hmc5883l import SensorHMC5338L

if __name__ == "__main__":
	config.init()
	shutdown = 0
	bus = smbus.SMBus(1)
	bmp085 = BMP085(bus,0x77,"BMP085")
	gyro = SensorITG3200(1,0x68)
	gyro.default_init()
	zeroX,zeroY,zeroZ = gyro.calibrate(1000,0.002)
	print 'Compass Initialization ... [Ok]'
	compass = SensorHMC5338L(1,0x1e)
	while not shutdown == 1: 
		input = raw_input("")
		if input == 'q':
			exit()
		if input == 'm':
			print "Bearing: ", compass.getBearing()
		if input == 'h':
			print '\tPress m to display compass values'
			print '\tPress p to display all available data'
			print '\tPress q to quit'
		if input == 'p':
			tempPress = bmp085.read_temperature_and_pressure()	
			gx,gy,gz = gyro.read_data_calib()
			print 'T\t%.2f\nP\t%.2f\nA\t%f' % (tempPress[0],tempPress[1],bmp085.readAltitude())
			print 'gx:\t%d\ngy:\t%d\ngz:\t%d' % (gx,gy,gz)
			print "Bearing: ", compass.getBearing()
