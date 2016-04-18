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
 

    __u8 reg = 0x32; /* Device register to access */
    float res;
    int16_t accZ;
    int N = 10;
    unsigned char values[6];

    float gainAccx2g =	0.0039;

for (int i = 0;i<N;i++)
{
  values[0] = i2c_smbus_read_word_data(file, reg);
  values[1] = i2c_smbus_read_word_data(file, 0x33);
  values[2] = i2c_smbus_read_byte_data(file, 0x34);
  values[3] = i2c_smbus_read_word_data(file, 0x35);
  values[4] = i2c_smbus_read_byte_data(file, 0x36);
  values[5] = i2c_smbus_read_byte_data(file, 0x37);

  // print out result
  printf("Values: X MSB: %d, X LSB: %d, Y MSB: %d, Y LSB: %d, Z MSB: %d, Z LSB: %d\n",
    values[0],values[1],values[2],values[3],values[4],values[5]);

    if (values[4] < 0 &&  values[5]<0) {
	printf("Fail");
    } else {

	accZ = (((int16_t)values[5]) << 8) | values[4];
        if (accZ & (1<<16-1))
            accZ  = accZ - (1<<16); 
	res = (float)  accZ * gainAccx2g * EARTH_GRAVITY_MS2;
        printf(" Data:  %f\n",res);
   }
   sleep(1);
}

/*
    for(int i = 0; i<4; i++) {
        // Using I2C Read
        if (read(file,buf,2) != 2) {
            printf("Failed to read from the i2c bus.\n");
            buffer = g_strerror(errno);
            printf(buffer);
            printf("\n\n");
        } else {
	    data = (((int16_t)buffer[1]) << 8) | buffer[0];
	    //if (data & (1<<16-1))
	//	data = data - (1<<16); 
            printf(" Data:  %04f\n",data);
        }
    }
*/
    //unsigned char reg = 0x10; // Device register to access
    //buf[0] = reg;
    
    /*
    if (write(file,buf,1) != 1) {
        // ERROR HANDLING: i2c transaction failed 
        printf("Failed to write to the i2c bus.\n");
        buffer = g_strerror(errno);
        printf(buffer);
        printf("\n\n");
    }*/
}

int main()
{
	ADXL345();	
	return 0;
}
