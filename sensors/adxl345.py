#!/usr/bin/python
from time import sleep
import smbus
import math

class adxl(object):
	
	def __init__(self, bus_nr, address):
		self.bus = smbus.SMBus(bus_nr)
		
		# This is the address read via i2cdetect
		self.address = address
		
		self.gainAccx = 0.0039
		self.gainAccy = 0.0039
		self.gainAccz = 0.0039
		
		# Power management registers
		self.power_mgmt_1 = 0x6b
		self.adxl345_power_ctl = 0x2d
		self.power_mgmt_2 = 0x6c
		self.adxl345_res_ctl = 0x31

		# Resolution modes:
		self.AFS_2g = 0
		self.AFS_4g = 1
		self.AFS_8g = 2
		self.AFS_16g = 3
		
		# Acc registers
		self.accx0 = 0x32
		self.accy0 = 0x34
		self.accz0 = 0x36
	
		# This is the address read via i2cdetect
		self.address = address
		
		# Now wake the 6050 up as it starts in sleep mode
		self.bus.write_byte_data(self.address, self.adxl345_power_ctl, 8)
		afs_scale = self.AFS_2g
		data_format = 1 << 3 | afs_scale
		self.bus.write_byte_data(self.address, self.adxl345_res_ctl, data_format)
		sleep(0.500)

	def get_y_rotation(self,x,y,z):
		radians = math.atan2(x, self.dist(y,z))
		return -math.degrees(radians)

	def get_x_rotation(self,x,y,z):
		radians = math.atan2(y, self.dist(x,z))
		return math.degrees(radians)

	def read_byte(self,adr):
	    return self.bus.read_byte_data(self.address, adr)

	def read_word(self,adr):
	    high = self.bus.read_byte_data(self.address, adr)
	    low = self.bus.read_byte_data(self.address, adr+1)
	    val = (high << 8) + low
	    return val

	def read_word_2c(self,adr):
	    val = self.read_word(adr)
	    if (val >= 0x8000):
	        return -((65535 - val) + 1)
	    else:
	        return val

	def dist(self,a,b):
	    return math.sqrt((a*a)+(b*b))

if __name__ == "__main__":
	import time
	shutdown = 0
	adx = adxl(1,0x53)	
	aTotX = 0
	aTotY = 0
	aTotZ = 0
	
	offx = -4928/( adx.gainAccx * 9.80665)
	offy = 4417 /( adx.gainAccx * 9.80665)
	offz = 530.6076 /( adx.gainAccx * 9.80665)

	while not shutdown == 100:
		shutdown = shutdown + 1
		
		#offx = adx.read_byte(0x1E)		
		#offy = adx.read_byte(0x1F)		
		#offz = adx.read_byte(0x20)		
		
		accel_xout = adx.read_word_2c(adx.accx0)
		accel_yout = adx.read_word_2c(adx.accy0)
		accel_zout = adx.read_word_2c(adx.accz0)

		accel_xout = accel_xout - offx
		accel_yout = accel_yout - offy
		accel_zout = accel_zout - offz
		
		#aTotX = aTotX + accel_xout
		#aTotY = aTotY + accel_yout
		#aTotZ = aTotZ + accel_zout

		accel_xout_scaled = accel_xout * adx.gainAccx
		accel_yout_scaled = accel_yout * adx.gainAccy
		accel_zout_scaled = accel_zout * adx.gainAccz
	
		accGX = accel_xout_scaled * 9.80665
		accGY = accel_yout_scaled * 9.80665
		accGZ = accel_zout_scaled * 9.80665
		print "\n\naccel_xout: ", accel_xout , "\t scaled: ", accel_xout_scaled, "\t g: ", accGX#, "\tOff: ", offx
		print "accel_yout: ", accel_yout , "\tscaled: ", accel_yout_scaled, "\t g: ", accGY#, "\tOff: ", offy
		print "accel_zout: ", accel_zout , "\t scaled: ", accel_zout_scaled, "\t g: ", accGZ#, "\tOff: ", offz
	
		print "\n\nx rotation: " , adx.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		print "y rotation: " , adx.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)	
		time.sleep(0.1)
	
	print "finished calibration\n\n"
	#print "Offset X: ", aTotX/100, "\tY: ", aTotY/100, "\tZ: " ,aTotZ/100

