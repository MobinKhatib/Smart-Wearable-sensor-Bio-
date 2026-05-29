/*
 * SPI_DMA_NAND.c
 *
 *  Created on: Jun 18, 2025
 *      Author: alice
 */


#include "SPI_DMA_NAND.h"
#include "string.h"
#include "stdio.h"
#include "stdbool.h"
#include "main.h"
#include "SPI.h"
#include "SPI_NAND.h"

extern SPI_HandleTypeDef hspi2;
//extern TIM_HandleTypeDef htim4;

// queste sono esterne
extern uint16_t bad_blocks[2048];

enum stati_dma{
    DMA_WRITE_ENABLE,
    DMA_PROGRAM_LOAD_CMD,
    DMA_PROGRAM_LOAD_DATA,
    DMA_PROGRAM_EXECUTE,
    DMA_DONE
    };
enum stati_dma stato_dma = DMA_DONE;

// queste cambiano solo qua!
static int write_dma_finish = -1;
static read_address_t blocco_dma;
static column_address_t colonna_dma = 0;
static uint8_t packet_prova[1023] ={0};
static int flag_page_complete=0;
static uint16_t n_blocco=0;
static uint8_t n_page=0;


void nand_dma_spi_callback(SPI_HandleTypeDef* hspi){
	switch (stato_dma) {
		case DMA_DONE:
		break;
		case DMA_WRITE_ENABLE:
			cs_deselect();
			stato_dma = DMA_PROGRAM_LOAD_CMD;
			uint8_t tx_data1[3];
			tx_data1[0] = CMD_PROGRAM_LOAD;
			cache_address_t data;
			data.dummy1 = 0;   // 3 dummy bits
			data.address = colonna_dma; // 13 address bits
			data.dummy2 = 0;   // 8 dummy bits
			tx_data1[1] = (data.whole >> 16) & 0xFF;
			tx_data1[2] = (data.whole >> 8) & 0xFF;
			cs_select();
			HAL_SPI_Transmit_DMA(hspi, tx_data1, 3);
		break;
		case DMA_PROGRAM_LOAD_CMD:
			//cs_deselect();
			stato_dma = DMA_PROGRAM_LOAD_DATA;
			//cs_select();
			HAL_SPI_Transmit_DMA(hspi, packet_prova, sizeof(packet_prova));
		break;
		case DMA_PROGRAM_LOAD_DATA:
			cs_deselect();
			stato_dma = DMA_PROGRAM_EXECUTE;
			uint8_t tx_data2[4];
			read_address_t row = blocco_dma;
			tx_data2[0] = CMD_PROGRAM_EXECUTE;
			tx_data2[1] = (row.whole >> 16) & 0xFF;
			tx_data2[2] = (row.whole >> 8) & 0xFF;
			tx_data2[3] = row.whole & 0xFF;
			cs_select();
			HAL_SPI_Transmit_DMA(hspi, tx_data2, 4);
		break;
		case DMA_PROGRAM_EXECUTE:
			cs_deselect();
			stato_dma = DMA_DONE;
			//HAL_TIM_Base_Start_IT(&htim4);
		break;
	}
}

void nand_dma_start_write(SPI_HandleTypeDef* hspi, const uint8_t *data_in) {
    stato_dma = DMA_WRITE_ENABLE;
	blocco_dma.block = bad_blocks[n_blocco];
	blocco_dma.page = n_page;

	memcpy(packet_prova, data_in, 1023);

	uint8_t cmd = CMD_WRITE_ENABLE;
	cs_select();
	HAL_SPI_Transmit_DMA(&hspi2, &cmd, 1);

	write_dma_finish = 0;
}

/*void nand_dma_timer_callback(TIM_HandleTypeDef* htim){
	poll_for_oip_clear(100); // in teoria questa dovrebbe essere già andata a posto e quindi non fa polling
	HAL_TIM_Base_Stop_IT(&htim4);

	// La pagina è completa? ho scritto i 4 chunck da 1023?
	if(flag_page_complete < 3){ // devo ancora scrivere
		write_dma_finish = -1; // stai nella scrittura
		flag_page_complete++;
		colonna_dma = colonna_dma+1024; // vai avanti con la colonna
	}

	else if(flag_page_complete==3){ // ho scritto 4 volte 1023 bytesquindi una pagina!
		flag_page_complete = 0;
		colonna_dma = 0; // devo ripartire da zero
		n_page ++; // avanzo di pagina

		write_dma_finish = -1;

		if (n_page==64){ // ho finito il blocco
			n_page = 0 ; //riparto dalla pagina zero
			n_blocco ++ ; // vado al blocco successivo

			if (n_blocco == 2048){
				write_dma_finish = 1;
			}
		}


	}
}*/

int8_t nand_dma_get_status(void) {
    return write_dma_finish;
}

void nand_dma_set_status(int8_t status) {
    write_dma_finish = status;
}
