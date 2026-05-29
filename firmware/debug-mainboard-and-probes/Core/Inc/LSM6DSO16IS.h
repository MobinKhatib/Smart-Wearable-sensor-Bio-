#ifndef __LSM6DSO16IS_H__
  #define __LSM6DSO16IS_H__
 
   /**
   * \file LSM6DSO16IS.h
   * \brief Library for LSM6DSO16IS IMU sensor by STMicrocontrollers
   *
   * */
 
    #define LSM6DSO16IS_I2C_ADDRESS 0x6B // SDO/SAO pin is connected to 3.3V
	#define LSM6DSO16IS_I2C_READ_ADDRESS 0xD7
	#define LSM6DSO16IS_I2C_WRITE_ADDRESS 0xD6
	#define LSM6DSO16IS_WHOAMI 0x0F
	#define LSM6DSO16IS_WHOAMI_VALUE 0x22
 
	#define LSMIS_ACC_CTRL1 0x10 // control register for ODR and FS selection on accelerometer
	#define LSMIS_GYR_CTRL2 0x11 // control register for ODR and FS selection on gyroscope
 
	#define LSMIS_GYR_CTRL7 0x16 // enable/disable high performance mode gyroscope
	#define LSMIS_ACC_CTRL6 0x15 // enable/disable high performance mode accelerometer
 
 
	#define LSMIS_OUTX_L_G 0x22    // Gyroscope LSB X register
	#define LSMIS_OUTX_H_G 0x23    // Gyroscope MSB X register
	#define LSMIS_OUTY_L_G 0x24    // Gyroscope LSB Y register
	#define LSMIS_OUTY_H_G 0x25    // Gyroscope MSB Y register
	#define LSMIS_OUTZ_L_G 0x26    // Gyroscope LSB Z register
	#define LSMIS_OUTZ_H_G 0x27    // Gyroscope MSB Z register
	#define LSMIS_OUTX_L_A 0x28    // Acceleration LSB Z register (first data register if auto-increment is enabled)
	#define LSMIS_OUTX_H_A 0x29    // Acceleration MSB Z register
	#define LSMIS_OUTY_L_A 0x2A    // Acceleration LSB Y register
	#define LSMIS_OUTY_H_A 0x2B    // Acceleration MSB Y register
	#define LSMIS_OUTZ_L_A 0x2C    // Acceleration LSB X register
	#define LSMIS_OUTZ_H_A 0x2D    // Acceleration MSB X register
 
	#define LSMIS_I2C_TIMEOUT 100
    #define FUNC_CFG_ACCESS 0x01
    #define ISPU_INT_STATUS 0x58
    #define ISPU_DOUT_00_L 0x10
    #define CTRL10_C 0x19
 
  //static uint8_t ispu_HSclock_en = 0x04;
  //static uint8_t ispu_LSclock_en = 0x00;
  //static uint8_t ispu_HSclock_Timestamp_en = 0x24;
  //static uint8_t ispu_LSclock_Timestamp_en = 0x20;
  //static uint8_t ispu_access_enable = 0x80;
  //static uint8_t ispu_access_disable = 0x00;
 
  uint8_t LSMIS_ReadRegister(uint8_t reg, uint8_t* reg_value, uint16_t buflen, I2C_HandleTypeDef *hi2c);
  uint8_t LSMIS_WriteRegister(uint8_t reg_addr, uint8_t reg_data, I2C_HandleTypeDef *hi2c);
  uint8_t LSMIS_BitMask(uint8_t reg_addr, uint8_t mask, uint8_t command, I2C_HandleTypeDef *hi2c);
 
 
#endif
