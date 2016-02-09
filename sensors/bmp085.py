#!/usr/bin/python
import smbus
import i2cutils as I2CUtils
import time

class BMP085(object):
    '''
    Simple BMP085 implementation
    Datasheet: http://www.adafruit.com/datasheets/BMP085_DataSheet_Rev.1.0_01July2008.pdf
    '''
    
    CALIB_BLOCK_ADDRESS = 0xAA
    CALIB_BLOCK_SIZE = 22
    
    def __init__(self, bus, address, name, oss=3):
        self.bus = bus
        self.address = address
        self.name = name
        self.temperature = 0
	self.pressure = 0
	self.altitude = 0
        self.calibration = I2CUtils.i2c_read_block(bus, address, BMP085.CALIB_BLOCK_ADDRESS, BMP085.CALIB_BLOCK_SIZE)
        self.oss = oss
        self.temp_wait_period = 0.004
        self.pressure_wait_period = 0.0255  # Conversion time


    def twos_compliment(self, val):
        if (val >= 0x8000):
            return -((0xffff - val) + 1)
        else:
            return val


    def test(self):
	print "\nok\n"
    
    def get_word(self, array, index, twos):
        val = (array[index] << 8) + array[index + 1]
        if twos:
            return self.twos_compliment(val)
        else:
            return val        
            
    def calculate(self):
        
        # The sensor has a block of factory set calibration values we need to read
        # these are then used in a length calculation to get the temperature and pressure
        # copy these into convenience variables
        ac1 = self.get_word(self.calibration, 0, True)
        ac2 = self.get_word(self.calibration, 2, True)
        ac3 = self.get_word(self.calibration, 4, True)
        ac4 = self.get_word(self.calibration, 6, False)
        ac5 = self.get_word(self.calibration, 8, False)
        ac6 = self.get_word(self.calibration, 10, False)
        b1 = self.get_word(self.calibration, 12, True)
        b2 = self.get_word(self.calibration, 14, True)
        mb = self.get_word(self.calibration, 16, True)
        mc = self.get_word(self.calibration, 18, True)
        md = self.get_word(self.calibration, 20, True)
        oss = self.oss
        
        # This code is a direct translation from the datasheet
        # and should be optimised for real world use
        
        # Read raw temperature
        I2CUtils.i2c_write_byte(self.bus, self.address, 0xF4, 0x2E)  # Tell the sensor to take a temperature reading
        time.sleep(self.temp_wait_period)  # Wait for the conversion to take place
        temp_raw = I2CUtils.i2c_read_word_signed(self.bus, self.address, 0xF6)
        
        I2CUtils.i2c_write_byte(self.bus, self.address, 0xF4, 0x34 + (self.oss << 6))  # Tell the sensor to take a pressure reading
        time.sleep(self.pressure_wait_period)  # Wait for the conversion to take place
        pressure_raw = ((I2CUtils.i2c_read_byte(self.bus, self.address, 0xF6) << 16) \
                     + (I2CUtils.i2c_read_byte(self.bus, self.address, 0xF7) << 8) \
                     + (I2CUtils.i2c_read_byte(self.bus, self.address, 0xF8))) >> (8 - self.oss)
        
        
        # Calculate temperature
        x1 = ((temp_raw - ac6) * ac5) / 32768
        x2 = (mc * 2048) / (x1 + md)
        b5 = x1 + x2
        t = (b5 + 8) / 16
        
        # Now calculate the pressure
        b6 = b5 - 4000 
        x1 = (b2 * (b6 * b6 >> 12)) >> 11
        x2 = ac2 * b6 >> 11
        x3 = x1 + x2
        b3 = (((ac1 * 4 + x3) << oss) + 2) >> 2 
        
        x1 = (ac3 * b6) >> 13 
        x2 = (b1 * (b6 * b6 >> 12)) >> 16 
        x3 = ((x1 + x2) + 2) >> 2 
        b4 = ac4 * (x3 + 32768) >> 15 
        b7 = (pressure_raw - b3) * (50000 >> oss)
        if (b7 < 0x80000000):
            p = (b7 * 2) / b4
        else:
            p = (b7 / b4) * 2
        x1 = (p >> 8) * (p >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        p = p + ((x1 + x2 + 3791) >> 4)
	self.temperature = t
	self.temperatureReadable = t/10.
	self.pressure = p 
	self.pressureReadable = p /100.
        return(t / 10., p / 100.)

    def read_pressure(self):
        (temperature, pressure) = self.calculate()
        return pressure 
    
    def read_temperature(self):
        (temperature, pressure) = self.calculate()
        return temperature 
    
    def read_temperature_and_pressure(self):
        return self.calculate()
     
        
    def readAltitude(self, seaLevelPressure=101325):
    	"Calculates the altitude in meters"
        #self.pressure = float(self.read_pressure())
	print "Pres %f" % self.pressure
        self.altitude = 44330.0 * (1.0 - pow(self.pressure / seaLevelPressure, 0.1903))
        return self.altitude

   
#if __name__ == "__main__":
    #bus = smbus.SMBus(1)
    #bmp085 = BMP085(bus, 0x77 , "BMP085") 
    #list = bmp085.read_temperature_and_pressure()
    #print 'Temperature: %.1f C \nPressure %.2f mbar' %(list[0],list[1])
    #print 'Estimated Altitude:  %.2f' % bmp085.readAltitude() 

    #print 'PressureR/N:  %.5f TempR/N : %.2f ' %(bmp085.pressure,bmp085.temperature)  
