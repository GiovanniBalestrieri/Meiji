#include <glib.h>
#include <glib/gprintf.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define EARTH_GRAVITY_MS2 9.80665
#define gainAccx2g	0.0039
float accX,accY,accZ;
int temp_value;

void ADXL345(void)
{
    int file;
    char filename[40];
    int addr = 0x53;        // The I2C address of the ADC
    int adapter_nr = 1; /* probably dynamically determined */
  
    snprintf(filename, 19, "/dev/i2c-%d", adapter_nr);
    file = open(filename, O_RDWR);
    if (file < 0)
    {
        printf("Failed to open the bus.");
		exit(1);
    }	

    if (ioctl(file,I2C_SLAVE,addr) < 0) {
        printf("Failed to acquire bus access and/or talk to slave.\n");
        exit(1);
    }
	
    /* Wake ADXL up
     * ADXL345 POWER_CTL Register */
    int i2c_dev_reg_addr = 0x2D;
 
    __s32 read_value;
    read_value = i2c_smbus_write_byte_data(file,i2c_dev_reg_addr,0x8);
    if (read_value < 0)
    {
	perror("I2C Write Operation failed.");
	exit(4);	
    }

    /* Set resolution */
    __u8 adxl345_res_ctl = 0x31;
    __u8 data_format = 0;

    i2c_smbus_write_byte_data(file,adxl345_res_ctl,data_format);
    sleep(0.500);
 	int gUnits = 1;

    __u8 reg = 0x32; /* Device register to access */
    int res = 0;
    int N = 10;

    char values[6];
	
	__s32 storage;	

	for (int i = 0;i<N;i++)
	{
		values[0] = i2c_smbus_read_byte_data(file, reg);
	  	values[1] = i2c_smbus_read_byte_data(file, 0x33);
		values[2] = i2c_smbus_read_byte_data(file, 0x34);
	 	values[3] = i2c_smbus_read_byte_data(file, 0x35);
	  	values[4] = i2c_smbus_read_byte_data(file, 0x36);
	  	values[5] = i2c_smbus_read_byte_data(file, 0x37);

	  	// print out result
	  	//printf("Values: X MSB: %d, X LSB: %d, Y MSB: %d, Y LSB: %d, Z MSB: %d, Z LSB: %d\n",
    	//values[0],values[1],values[2],values[3],values[4],values[5]);

		if (storage<0) {
			// #Error Handling
		} else {
			// Read and compose 16 bytes long (two-compliment) 
			// acceleration
		}
		
	    //if (values[4] < 0 &&  values[5]<0) {
		if (values < 0) {
		printf("Fail");
	    } else {
			fromBuffer2Acc(values,gUnits);
	    	printf(" Data: %f \t %f \t %f\n",accX,accY,accZ);
	   }
 	   sleep(1);
	}
}

/*
 *	Interprets the 16 bit value a (positive or negative) two's
 *  complement
 *  PARAM
 * 		@CHAR array of bytes	
 *		@BOOL converts to G if true
 */
int fromBuffer2Acc(char buffer[],int gs)
{
	temp_value = (((int16_t)buffer[1]) << 8) | buffer[0];
	if (temp_value & (1<<16-1))
		temp_value  = temp_value - (1<<16);
	if (gs)
		accX = (float)  temp_value * gainAccx2g * EARTH_GRAVITY_MS2;

	temp_value = (((int16_t)buffer[3]) << 8) | buffer[2];
	if (temp_value & (1<<16-1))
		temp_value  = temp_value - (1<<16);
	if (gs)
		accY = (float)  temp_value * gainAccx2g * EARTH_GRAVITY_MS2;

	temp_value = (((int16_t)buffer[5]) << 8) | buffer[4];
	if (temp_value & (1<<16-1))
		temp_value  = temp_value - (1<<16);
	if (gs)
		accZ = (float)  temp_value * gainAccx2g * EARTH_GRAVITY_MS2;
	
	return 1;
}

int main()
{
	ADXL345();	
	return 0;
}
