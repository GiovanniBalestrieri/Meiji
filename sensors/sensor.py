#!/usr/bin/python
from time import sleep
import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
adxl345_power_ctl = 0x2d
power_mgmt_2 = 0x6c

# Acc registers
accx0 = 0x32
accy0 = 0x34
accz0 = 0x36


gainAccx = 0.00376390
gainAccy = 0.00376009
gainAccz = 0.00349265

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

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def initGyro(addGyro,rateDiv,rangeW,filterBW,clockSrc):
	# Set sample rate divisor
	
	bus.write_byte_data(addGyro, SMPLRT_DIV , rateDiv)
	bus.write_byte_data(addGyro, DLPF_FS , 9 )
	bus.write_byte_data(addGyro, DLPF_FS, 8)
	bus.write_byte_data(addGyro, PWR_MGM, 8)
	bus.write_byte_data(addGyro, INT_CFG, 8)
	bus.write_byte_data(addGyro, INT_CFG, 8)
	

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x53       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, adxl345_power_ctl, 8)
sleep(0.500)
print "gyro data"
print "---------"

gyro_xout = read_word_2c(0x43)
gyro_yout = read_word_2c(0x45)
gyro_zout = read_word_2c(0x47)

print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

print
print "accelerometer data"
print "------------------"

accel_xout = read_word_2c(accx0)
accel_yout = read_word_2c(accy0)
accel_zout = read_word_2c(accz0)

accel_xout_scaled = accel_xout * gainAccx
accel_yout_scaled = accel_yout * gainAccy
accel_zout_scaled = accel_zout * gainAccz

print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

