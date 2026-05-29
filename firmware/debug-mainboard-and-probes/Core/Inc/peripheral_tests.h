/*******************************************************************************
 * @file    peripheral_tests.h
 * @author  Ilaria Crupi
 * @date    29-Aug-2025
 * @brief   Header for the test functions of sensors and peripherals connected
 * to the various system boards.
 *
 * This file declares all the test functions used to verify the
 * communication and correct operation of the sensors and peripherals:
 *
 * - MAIN BOARD
 * - LED Control
 * - test_USB_TX()
 * - test_BLE()
 * - test_NAND()
 * - test_IMU_IS()
 *
 *
 * The RUN_XXX_TEST macros allow enabling or disabling individual tests
 * from main() or the while(1) loop.
 *
 ******************************************************************************/

#ifndef PERIPHERAL_TESTS_H
#define PERIPHERAL_TESTS_H

#include "main.h"

// --- TEST CONTROL PANEL ---
// Set to 1 to run the test, 0 to skip it.

#define RUN_USB_TEST        1
#define RUN_BLE_TEST        1
#define RUN_NAND_TEST       1
#define RUN_IMU_IS_TEST     1

// --- TEST FUNCTION DECLARATIONS ---

// MAIN BOARD
void test_USB_TX(void);
void test_BLE(UART_HandleTypeDef *huart);
void test_NAND(void);
void test_IMU_IS(I2C_HandleTypeDef *hi2c);

#endif // PERIPHERAL_TESTS_H