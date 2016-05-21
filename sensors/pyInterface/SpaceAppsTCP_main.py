#!/usr/bin/python

import config
import socket
import sys
import time
from thread import *
import smbus,time
import i2cutils as I2CUtils
from bmp085 import BMP085
from itg3200 import SensorITG3200
from hmc5883l import SensorHMC5338L
from adxl345 import Adxl

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8881  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome\n')
     
    #infinite loop so that function doesn't terminate and thread ends.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = "a," + str(1.30) + "," + str(3.4) +",z"
        if not data: 
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()


def helpInfo():
	print '\n\n\tHelp: Press'
	print '\t\t m to display compass values'
	print '\t\t t to display all available data'
	print '\t\t r to show estimated Roll angle'
	print '\t\t p to show estimated Pitch angle'
	print '\t\t a to show accelerations'
	print '\t\t b to display barometer values'
	print '\t\t q to quit'

def send_array(conn, data):
	reply = ""
	for i in range(len(data) - 1):
		reply = reply + str(data[i]) + " : "
	reply = reply + str(data[i+1])
	conn.sendall(reply)	
	print "Sent: \t", reply


def send_value(conn, value):
	reply = "a," + str(value) + ",z"
	conn.sendall(reply)

def wait_for_ack(conn):
	data = conn.recv(1024);
	while ((data == 0) or (data != 99)):
		print "RECEIVED: " + str(data)
		data = conn.recv(1024);
	print "OK, all good!"

if __name__ == "__main__":
	#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock = socket.create_connection("192.168.43.39")
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	print "Conn: ", conn
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
		data = []
		data.append(adx.getRoll())
		data.append(adx.getPitch())
		data.append(compass.getBearing())
		time.sleep(0.1)
		send_array(conn, data)
		continue		

		axes = adx.getAxes()
		gx,gy,gz = gyro.read_data_calib()
		mx,my,mz = compass.read_data()
		data.append(axes['x'])
		data.append(axes['y'])
		data.append(axes['z'])
		data.append(gx)
		data.append(gy)
		data.append(gz)
		data.append(mx)
		data.append(my)
		data.append(mz)
		time.sleep(0.1)
		send_array(conn, data)
#		wait_for_ack(conn);

	while not shutdown == 1: 
		input = raw_input("")
		if input == 'q':
			exit()
		if input == 'a':
			axes = adx.getAxes()
	                axesG = adx.toG(axes)
	        	send_array(conn, axes)
		        print "\n\nAcc X: ", axes['x'] , "m/s^2"
       			print "Acc X: ", axesG['x'], "G\t"

	       	        print "\n\nAcc Y: ", axes['y'] , "m/s^2"
	        	print "Acc Y: ", axesG['y'], "G\t"

		        print "\n\nAcc Z: ", axes['z'] , "m/s^2"
            		print "Acc Z: ", axesG['z'], "G\t"

		if input == 'r':
			roll = adx.getRoll()
		        send_value(conn, roll)
		        print "\n\nx rotation: " , roll
		if input == 'p':
			pitch = adx.getPitch()
	                send_value(conn, pitch)
        	        print "y rotation: " , pitch
		if input == 'm':
			bearing = compass.getBearing()
			send_value(conn, bearing)
			print "Bearing: ", bearing
		if input == 'h':
			helpInfo()
		if input == 'b':
			data = bmp085.read_temperature_and_pressure()	
			data.append(bmp085.readAltitude())
			send_array(conn, data)
			print 'T\t%.2f\nP\t%.2f\nA\t%f' % (data[0],data[1],data(2))
		if input == 't':
			print "All data from the IMU: "
			tempPress = bmp085.read_temperature_and_pressure()	
			gx,gy,gz = gyro.read_data_calib()
			print 'T\t%.2f\nP\t%.2f\nA\t%f' % (tempPress[0],tempPress[1],bmp085.readAltitude(1016101610161016101610161016101610161016))
			print 'gx:\t%d\ngy:\t%d\ngz:\t%d' % (gx,gy,gz)
			print "Bearing: ", compass.getBearing()
			
            		print "x rotation: " , adx.getRoll()
		        print "y rotation: " , adx.getPitch()
		if input == 'c':
			conn.close()
			print "Connection closed\n"
