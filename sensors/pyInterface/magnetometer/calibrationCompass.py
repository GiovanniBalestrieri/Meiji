#!/usr/bin/python
import smbus, time, math, csv
import sys
sys.path.append('../')
import i2cutils

deuxieme_tour = False
bus = smbus.SMBus(1)
address = 0x1e
max_val = [0,0,0] 
min_val = [0,0,0]
bias = [0,0,0]
mag_scale_pre = [0,0,0]
mag_scale = [0,0,0]

# Set to 8 samples @ 15Hz
i2cutils.i2c_write_byte(bus,address,0, 0b01110000) 
# 1.3 gain LSb / Gauss 1090 (default)
i2cutils.i2c_write_byte(bus,address,1, 0b00100000)
# Continuous sampling
i2cutils.i2c_write_byte(bus,address,2, 0b00000000)

scale = 0.92
readings = [0,0,0] 

with open("calibrate_values.csv","wb") as csv_file:
    writer = csv.writer(csv_file,delimiter=',')
    for i in range(0,800):
        x_out = i2cutils.i2c_read_word_signed(bus,address,3)*scale
        y_out = i2cutils.i2c_read_word_signed(bus,address,7)*scale
        z_out = i2cutils.i2c_read_word_signed(bus,address,5)*scale

        readings[0] = x_out
        readings[1] = y_out
        readings[2] = z_out

        for i in range(3):
            if readings[i] > max_val[i]:
                max_val[i] = readings[i]

            if readings[i] < min_val[i]:
                min_val[i] = readings[i]
    
        bearing  = math.atan2(y_out, x_out) 
        if (bearing < 0):
            bearing += 2 * math.pi
    
        print x_out, y_out, z_out, math.degrees(bearing)#, (x_out * scale), (y_out * scale), bearing
        data = ['a',x_out,y_out,z_out,bearing,'z']
        writer.writerow(data)
        time.sleep(0.1)

print("Calibration done: min: " +str(min_val) + " max: " + str(max_val))
print("Getting hard iron corrections ...")


for i in range(3):
    bias[i] = (max_val[i] + min_val[i])/2
    mag_scale_pre[i] = (max_val[i] - min_val[i])/2


print(bias)

print("Getting soft Iron correcitons")
print("mag_pre_scale : " + str(mag_scale_pre))
avg = sum(mag_scale_pre)/3
print("AVG: " + str(avg))
for i in range(3):
    mag_scale[i] = avg/float(mag_scale_pre[i])
            
print(mag_scale)

with open("config_mag.csv","wb") as csv_file:
    writer = csv.writer(csv_file,delimiter=',')
    data=['b',bias[0],bias[1],bias[2],'z']
    data2=['s',mag_scale[0],mag_scale[1],mag_scale[2]]
    writer.writerow(data)
    writer.writerow(data2)
    print("saved calibration results")

print("Calibrated Values: ")
time.sleep(2)
if deuxieme_tour:
    with open("calibrated_values.csv","wb") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        for i in range(0,400):
            x_out = i2cutils.i2c_read_word_signed(bus,address,3)*scale
            y_out = i2cutils.i2c_read_word_signed(bus,address,7)*scale
            z_out = i2cutils.i2c_read_word_signed(bus,address,5)*scale
        
            x = (x_out - bias[0])*mag_scale[0]
            y = (y_out - bias[1])*mag_scale[1]
            z = (z_out - bias[2])*mag_scale[2]
        
            bearing  = math.atan2(y, x) 
            bearing_raw = math.atan2(y_out, x_out) 
            if (bearing < 0):
                bearing += 2 * math.pi
            if (bearing_raw < 0):
                bearing_raw += 2 * math.pi
            
            print x_out, y_out, z_out, (x), (y), z, bearing_raw , bearing
            data= [x_out, y_out, z_out, (x), (y), z, bearing_raw , bearing]
            writer.writerow(data)
            time.sleep(0.1)
 
