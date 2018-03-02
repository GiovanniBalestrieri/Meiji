#!/usr/bin/python
import smbus, time, math, csv

bus = smbus.SMBus(1)
address = 0x1e

bias=[0,0,0]
scales=[1,1,1]

with open("config_mag.csv",'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        if row[0]=='b':
            for i in range(3):
                bias[i] = row[i+1]
        elif row[0] == 's':
            for i in range(3):
                scales[i] = row[i+1]
print("Getting configuration .../n Bias: " + str(bias) + " scales: " + str(scales))

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

write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92

for i in range(0,200):
	time.sleep(0.1)
	x_out = read_word_2c(3) * scale
	y_out = read_word_2c(7) * scale
	z_out = read_word_2c(5) * scale

	bearing  = math.atan2(y_out, x_out) 
	if (bearing < 0):
	    bearing += 2 * math.pi
	print "Bearing: ", math.degrees(bearing)

