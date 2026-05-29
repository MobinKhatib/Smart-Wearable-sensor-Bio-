/*
 * LSM6DSO16IS.c
 *
 *  Created on: Apr 29, 2024
 *      Author: alice
 */

#include "main.h"
#include "LSM6DSO16IS.h"
#include "string.h"
#include "stdio.h"

// Helper Functions

// Helper function to read a register from LSM6DSV16BX IMU
uint8_t LSMIS_ReadRegister(uint8_t reg, uint8_t* reg_value, uint16_t buflen, I2C_HandleTypeDef *hi2c)
{
    uint8_t result = 1;
    uint8_t reg_addr = reg;  // Address of the register we want to access

    HAL_I2C_Master_Transmit(hi2c, LSM6DSO16IS_I2C_WRITE_ADDRESS, &reg_addr, sizeof(reg_addr), I2C_TIMEOUT);
    if(HAL_I2C_Master_Receive(hi2c, LSM6DSO16IS_I2C_READ_ADDRESS, reg_value, buflen, I2C_TIMEOUT) == HAL_OK)
    {
        return result;
    }
    else
    {
        return 0;
    }
}

// Helper function to write a register in MAX30101
uint8_t LSMIS_WriteRegister(uint8_t reg_addr, uint8_t reg_data, I2C_HandleTypeDef *hi2c)
{
    uint8_t result = 1;
    uint8_t LSMIS_Register[] = {reg_addr, reg_data};  // Register we would like to write on and relative data

    if(HAL_I2C_Master_Transmit(hi2c, LSM6DSO16IS_I2C_WRITE_ADDRESS, LSMIS_Register, 2, I2C_TIMEOUT) != HAL_OK)
    {
        result = 0;
    }
    return result;
}

// Helper function to perform bit mask operations
// Inputs: Register address, mask, command to write (enable/disable)
uint8_t LSMIS_BitMask(uint8_t reg_addr, uint8_t mask, uint8_t command, I2C_HandleTypeDef *hi2c)
{
    uint8_t reg_data=0;
    uint8_t result = LSMIS_ReadRegister(reg_addr, &reg_data, sizeof(reg_data), hi2c);
    if (result)
    {
        reg_data = reg_data & mask;
        reg_data = reg_data | command;

        result = LSMIS_WriteRegister(reg_addr, reg_data,hi2c);

    }
    return result;
}

