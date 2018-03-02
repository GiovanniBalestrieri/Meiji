#!/usr/bin/python

import smbus,time,math,csv, i2cutils

bus = smbus.SMBus(1)
address = 0x1e


def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)


class SensorHMC5338L(object):
	def __init__(self,busNr,addr):
		self.bus = smbus.SMBus(busNr)
		self.address = addr

		# Set to 8 samples @ 15Hz
		i2cutils.i2c_write_byte(bus,address,0, 0b01110000) 
		# 1.3 gain LSb / Gauss 1090 (default)
		i2cutils.i2c_write_byte(bus,address,1, 0b00100000) 
		# Continous sampling
		i2cutils.i2c_write_byte(bus,address,2, 0b00000000)

                self.using_configs = False
                self.bias = [0,0,0]
                self.scales = [1,1,1]
		self.scale = 0.92
                self.load_config()

        def load_config(self):
            try:
                with open("config_mag_good_4_toutilo.csv",'rb') as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    bias_read = False
                    scale_read = False
                    for row in reader:
                        if row[0]=='b':
                            for i in range(3):
                                self.bias[i] = float(row[i+1])
                            bias_read = True
                        elif row[0] == 's':
                            for i in range(3):
                                self.scales[i] = float(row[i+1])
                            scale_read = True
                    if scale_read and bias_read:
                        self.using_configs = True
                    print("Getting configuration .../n Bias:/n " + str(self.bias) + "/n scales:/n " + str(self.scales))
            except:
                print("No magnetometer configuration file found. Using factory values")
                pass

	def read_data(self):	
		x_out = i2cutils.i2c_read_word_signed(bus,address,3) * self.scale
		y_out = i2cutils.i2c_read_word_signed(bus,address,7) * self.scale
		z_out = i2cutils.i2c_read_word_signed(bus,address,5) * self.scale
		return(x_out,y_out,z_out)

	def getBearing(self):
		mx,my,mz = self.read_data()
		bearing  = math.atan2(my,mx) 
		if (bearing < 0):
		    bearing += 2 * math.pi
		return math.degrees(bearing)

if __name__ == '__main__':
	print 'Welcome to HMC5883L sensor driver!\n\nPress h for help'
	shut = 0
	compass = SensorHMC5338L(1,0x1e)
	while not shut == 1:
		input = raw_input("")
		if input == 'q':
			print 'Bye'
			exit()
		if input == 'h':
			print '\t Press m to show 200 values of the yaw angle'
		if input == 'm':
		for i in range(0,200):
				time.sleep(0.1)
		        	print "Bearing: ", compass.getBearing()
		
