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
#include <math.h>

#define EARTH_GRAVITY_MS2 9.80665
#define gainAccx2g	0.0039
#define offAccX 0.4666
#define offAccY -0.1594
#define offAccZ -0.7343
#define X_INDEX 0
#define Y_INDEX 1
#define Z_INDEX 2


float accX,accY,accZ;
float acc[3];
float roll,pitch,yaw;
int temp_value;

#ifndef M_PI 
	#define M_PI 3.1415926535 
#endif

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
	if (temp_value & (1<<(16-1)))
		temp_value  = temp_value - (1<<16);
	if (gs){
		//temp_value =  temp_value - offAccX;
		accX = (float)  temp_value * gainAccx2g * EARTH_GRAVITY_MS2;
	}

	temp_value = (((int16_t)buffer[3]) << 8) | buffer[2];
	if (temp_value & (1<<(16-1)))
		temp_value  = temp_value - (1<<16);
	if (gs){
		//temp_value =  temp_value - offAccY;
		accY = (float)  temp_value * gainAccx2g * EARTH_GRAVITY_MS2;
	}

	temp_value = (((int16_t)buffer[5]) << 8) | buffer[4];
	if (temp_value & (1<<(16-1)))
		temp_value  = temp_value - (1<<16);
	if (gs){
	 	//temp_value = temp_value - offAccZ;	
		accZ = (float)  temp_value * gainAccx2g * EARTH_GRAVITY_MS2;
	}
	return 1;
}



/* 
 *	Computes the distance between two points_ euclidean norm
 *  PARAM 
 *  	@FLOAT point A
 *		@FLOAT point B
 *  RETURNS
 *		@FLOAT distance
 */
double dist(float a,float b) {
   return sqrt( (a*a)+(b*b));
}


/* 
 *	Converts from radians to degree
 *  PARAM 
 *  	@FLOAT radians
 *  RETURNS
 *		@FLOAT degree
 */
float toDegree(float radians) {
	float deg = radians * (180.0 / M_PI);
	return deg;
}

/*
 *	Computes angular position along the X axis from acc data
 *  PARAM
 * 		@FLOAT X,Y,Z	
 *	RETURNS
 *		@FLOAT Roll
 */
float getXRotation(float acc[3])
{
	float radians = atan2(acc[Y_INDEX], (double) dist(acc[X_INDEX],acc[Z_INDEX]));
	return toDegree(radians);
}

/*
 *	Computes roll angle from a trigonometric approach
 *  PARAM
 * 		@FLOAT X,Y,Z	
 *	RETURNS
 *		@FLOAT Roll
 */
float getRoll(float acc[])
{
	float roll = getXRotation(acc);
	return roll;
}

/*
 *	Computes angular position along the Y axis from acc data
 *  PARAM
 * 		@FLOAT X,Y,Z	
 *	RETURNS
 *		@FLOAT Pitch
 */
float getYRotation(float acc[])
{
	float radians = atan2(acc[X_INDEX], (double) dist(acc[Y_INDEX],acc[Z_INDEX]));
	return toDegree(radians);
}

/*
 *	Computes pitch angle from a trigonometric approach
 *  PARAM
 * 		@FLOAT X,Y,Z	
 *	RETURNS
 *		@FLOAT Roll
 */
float getPitch(float acc[])
{
	float pitch = getYRotation(acc);
	return pitch;
}


int ADXL345(void)
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
	
	return file;

}

void readAdxl(int file)
{
	/* Device register to access */
    __u8 reg = 0x32; 
 	int gUnits = 1;
    char values[6];

	/* Read bytes from sensor */
	values[0] = i2c_smbus_read_byte_data(file, reg);
  	values[1] = i2c_smbus_read_byte_data(file, 0x33);
	values[2] = i2c_smbus_read_byte_data(file, 0x34);
 	values[3] = i2c_smbus_read_byte_data(file, 0x35);
  	values[4] = i2c_smbus_read_byte_data(file, 0x36);
  	values[5] = i2c_smbus_read_byte_data(file, 0x37);

	if (values<0) {
		// #Error Handling
		printf("Fail!!");
	} else {
		// Read and compose 16 bytes long (two-compliment) 
		// acceleration
		fromBuffer2Acc(values,gUnits);
		acc[0] = accX;
		acc[1] = accY;
		acc[2] = accZ;
		roll = getRoll(acc);
		pitch = getPitch(acc);
	}
    usleep(100000);
}

int main()
{
	int adxl345 = ADXL345();	
    int N = 100;
	for (int i = 0;i<N;i++)
	{
		readAdxl(adxl345);
		printf("\nData: %f \t %f \t %f",accX,accY,accZ);
		printf("\tRoll: %f \t Pitch: %f \n",roll,pitch);
	}
	return 0;
}
