/*
 * SPI_DMA_NAND.h
 *
 *  Created on: Jun 18, 2025
 *      Author: alice
 */

#ifndef INC_SPI_DMA_NAND_H_
#define INC_SPI_DMA_NAND_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "string.h"
#include "stdio.h"
#include "main.h"
#include "SPI.h"
#include "SPI_NAND.h"


//void nand_dma_timer_callback(TIM_HandleTypeDef* htim);
void nand_dma_start_write(SPI_HandleTypeDef* hspi, const uint8_t *data_in);
void nand_dma_spi_callback(SPI_HandleTypeDef* hspi);
int8_t nand_dma_get_status(void);
void nand_dma_set_status(int8_t status);

#endif /* INC_SPI_DMA_NAND_H_ */
