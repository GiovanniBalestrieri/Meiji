#!/usr/bin/python
import time
from time import sleep
import smbus
import math

logpath = '/home/userk/sensors/Meiji/sensors/log/acc.csv'
logpathRaw = '/home/userk/sensors/Meiji/sensors/log/accRaw.csv'

class adxl(object):
	
	def __init__(self, bus_nr, address):
		self.bus = smbus.SMBus(bus_nr)
		
		# This is the address read via i2cdetect
		self.address = address
		
		# Unwrapping tolerance
		self.Ztol2g = 32384 #32384
		self.Xtol2g = 32256
		self.Ytol2g = 32128

		self.gainAccx2g = 0.0039
		self.gainAccy2g = 0.0039
		self.gainAccz2g = 0.0039
		
		
		self.gainAccx16g = 0.0312
		self.gainAccy16g = 0.0312
		self.gainAccz16g = 0.0312

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
		data_format = afs_scale  # Set Full Res + G res
		data_format =  afs_scale
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

	def unwrap(self,past,actual,tol):
	    #Upward unwrapping
	    if (past - actual > tol):
	        actual = actual + 2*tol;
	    #Downward wrapping
	    if (actual - past > tol):
	        actual = actual - 2*tol
	    return actual

if __name__ == "__main__":
	f = open(logpath,'w+')
	F = open(logpathRaw,'w+')
	shutdown = 0
	N = 200

	adx = adxl(1,0x53)	

	aTotX = 0
	aTotY = 0
	aTotZ = 0
	
	accXM1 = 0
	accYM1 = 0
	accZM1 = 0

	#offx = -4928/( adx.gainAccx * 9.80665)
	#offy = 4417 /( adx.gainAccx * 9.80665)
	#offz = 530.6076 /( adx.gainAccx * 9.80665)

	offx = 322#*adx.gainAccx
	offy = -850#*adx.gainAccy
	offz = -13295#*adx.gainAccz

	while not shutdown == N:
		shutdown = shutdown + 1
		
		#offx = adx.read_byte(0x1E)		
		#offy = adx.read_byte(0x1F)		
		#offz = adx.read_byte(0x20)		
		
		accel_xout = adx.read_word_2c(adx.accx0)
		accel_yout = adx.read_word_2c(adx.accy0)
		accel_zout = adx.read_word_2c(adx.accz0)
	
		accel_zoutF = adx.unwrap(accZM1,accel_zout,adx.Ztol2g)
		accel_xoutF = adx.unwrap(accXM1,accel_xout,adx.Xtol2g)
		accel_youtF = adx.unwrap(accYM1,accel_yout,adx.Ytol2g)
	
		accXM1 = accel_xoutF
		accYM1 = accel_youtF
		accZM1 = accel_zoutF
		
		#accel_xout = accel_xout - offx
		#accel_yout = accel_yout - offy
		#accel_zout = accel_zout - offz

		#accX = (accel_xout)*invGainx
		#accY = (accel_yout)*invGainy
		#accZ = (accel_zout)*invGainz
		
		aTotX = aTotX + accel_xout
		aTotY = aTotY + accel_yout
		aTotZ = aTotZ + accel_zout
		
		accel_xout_scaled = accel_xout * adx.gainAccx2g
		accel_yout_scaled = accel_yout * adx.gainAccy2g
		accel_zout_scaled = accel_zout * adx.gainAccz2g
	
		accGX = accel_xout_scaled * 9.80665
		accGY = accel_yout_scaled * 9.80665
		accGZ = accel_zout_scaled * 9.80665
		
		print "\n\naccel_xout: ", accel_xout , "\t scaled: ", accel_xout_scaled, "\t g: ", accGX#, "\tOff: ", offx
		print "accel_yout: ", accel_yout , "\tscaled: ", accel_yout_scaled, "\t g: ", accGY#, "\tOff: ", offy
		print "accel_zout: ", accel_zout , "\t scaled: ", accel_zout_scaled, "\t g: ", accGZ#, "\tOff: ", offz
	
		print "\n\nx rotation: " , adx.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		print "y rotation: " , adx.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)	
		
		#print "\n\n Accs: ",accX , "\t", accY, "\t", accZ
		
		F.write('A,')
		F.write(str(accel_xout))
		F.write(',') 
		F.write(str(accel_yout))
		F.write(',') 
		F.write(str(accel_zout))
		F.write(',')
		F.write(str(shutdown))
		F.write(',z\n')

		f.write('A,')
		f.write(str(accel_xoutF))
		f.write(',') 
		f.write(str(accel_youtF))
		f.write(',') 
		f.write(str(accel_zoutF))
		f.write(',')
		f.write(str(shutdown))
		f.write(',z\n')
		time.sleep(0.1)
	
	print "finished calibration\n\n"

	print "X0 = ", aTotX/N
	print "Y0 = ", aTotY/N
	print "Z0 = ", aTotZ/N
	
#print "Offset X: ", aTotX/100, "\tY: ", aTotY/100, "\tZ: " ,aTotZ/100
	f.close()
	F.close()
