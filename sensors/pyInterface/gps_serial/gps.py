#! /usr/bin/env python

import serial
import time

ser = serial.Serial('/dev/ttyAMA0',baudrate=9600, timeout=2)
time.sleep(1)

def read_serial():
    try:
        while True:
            #if ser.inWaiting() > 0:
            print("arriva")
            data = ser.readline()
            print(data)
    except IOError:
        print('cannot open')
    finally:
        print("Closing")
        ser.close()
        pass

read_serial()
