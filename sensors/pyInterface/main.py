#!/usr/bin/python

import config
import smbus,time
import i2cutils as I2CUtils
from bmp085 import BMP085
from itg3200 import SensorITG3200
from hmc5883l import SensorHMC5338L
from adxl345 import Adxl

def helpInfo():
	print '\n\n\tHelp: Press'
	print '\t\t m to display compass values'
	print '\t\t t to display all available data'
	print '\t\t r to show estimated Roll angle'
	print '\t\t p to show estimated Pitch angle'
	print '\t\t a to show accelerations'
	print '\t\t b to display barometer values'
	print '\t\t q to quit'

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
		
	# Accelerometer:
	# adxl(i2c_adapter,bus_nr,resolution)
        # resolution:      [0,1,2,3] for [2g,4g,8g,16g]
        adx = Adxl(1,0x53,0)
	helpInfo()	

	while not shutdown == 1: 
		input = raw_input("")
		if input == 'q':
			exit()
		if input == 'a':
			axes = adx.getAxes()
	                axesG = adx.toG(axes)
        	        print "\n\nAcc X: ", axes['x'] , "m/s^2"
               		print "Acc X: ", axesG['x'], "G\t"

	                print "\n\nAcc Y: ", axes['y'] , "m/s^2"
	                print "Acc Y: ", axesG['y'], "G\t"

        	        print "\n\nAcc Z: ", axes['z'] , "m/s^2"
	                print "Acc Z: ", axesG['z'], "G\t"

		if input == 'r':
        	        print "\n\nx rotation: " , adx.getRoll()
		if input == 'p':
	                print "y rotation: " , adx.getPitch()
		if input == 'm':
			print "Bearing: ", compass.getBearing()
		if input == 'h':
			helpInfo()
		if input == 'b':
			tempPress = bmp085.read_temperature_and_pressure()	
			print 'T\t%.2f\nP\t%.2f\nA\t%f' % (tempPress[0],tempPress[1],bmp085.readAltitude())
		if input == 't':
			print "All data from the IMU: "
			tempPress = bmp085.read_temperature_and_pressure()	
			gx,gy,gz = gyro.read_data_calib()
			print 'T\t%.2f\nP\t%.2f\nA\t%f' % (tempPress[0],tempPress[1],bmp085.readAltitude(1016101610161016101610161016101610161016))
			print 'gx:\t%d\ngy:\t%d\ngz:\t%d' % (gx,gy,gz)
			print "Bearing: ", compass.getBearing()
			
	                print "x rotation: " , adx.getRoll()
	                print "y rotation: " , adx.getPitch()
			
			
