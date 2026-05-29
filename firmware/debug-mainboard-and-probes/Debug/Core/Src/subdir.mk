################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/AS7331.c \
../Core/Src/AS7341.c \
../Core/Src/Bluetooth.c \
../Core/Src/DPS310XTSA1.c \
../Core/Src/IIS2MDC.c \
../Core/Src/LSM6DSO16IS.c \
../Core/Src/LSM6DSV16BX.c \
../Core/Src/MAX30101.c \
../Core/Src/MAX30205.c \
../Core/Src/SPI_DMA_NAND.c \
../Core/Src/SPI_NAND.c \
../Core/Src/main.c \
../Core/Src/peripheral_tests.c \
../Core/Src/stm32u5xx_hal_msp.c \
../Core/Src/stm32u5xx_it.c \
../Core/Src/syscalls.c \
../Core/Src/sysmem.c \
../Core/Src/system_stm32u5xx.c 

OBJS += \
./Core/Src/AS7331.o \
./Core/Src/AS7341.o \
./Core/Src/Bluetooth.o \
./Core/Src/DPS310XTSA1.o \
./Core/Src/IIS2MDC.o \
./Core/Src/LSM6DSO16IS.o \
./Core/Src/LSM6DSV16BX.o \
./Core/Src/MAX30101.o \
./Core/Src/MAX30205.o \
./Core/Src/SPI_DMA_NAND.o \
./Core/Src/SPI_NAND.o \
./Core/Src/main.o \
./Core/Src/peripheral_tests.o \
./Core/Src/stm32u5xx_hal_msp.o \
./Core/Src/stm32u5xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32u5xx.o 

C_DEPS += \
./Core/Src/AS7331.d \
./Core/Src/AS7341.d \
./Core/Src/Bluetooth.d \
./Core/Src/DPS310XTSA1.d \
./Core/Src/IIS2MDC.d \
./Core/Src/LSM6DSO16IS.d \
./Core/Src/LSM6DSV16BX.d \
./Core/Src/MAX30101.d \
./Core/Src/MAX30205.d \
./Core/Src/SPI_DMA_NAND.d \
./Core/Src/SPI_NAND.d \
./Core/Src/main.d \
./Core/Src/peripheral_tests.d \
./Core/Src/stm32u5xx_hal_msp.d \
./Core/Src/stm32u5xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32u5xx.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o Core/Src/%.su Core/Src/%.cyclo: ../Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m33 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32U575xx -c -I../Core/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc -I../Drivers/STM32U5xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32U5xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/ila10/OneDrive - Politecnico di Milano/Documenti/PoliMi/SEL/Smart Wearables/Debug_Narwhal/USB_Device" -I"C:/Users/ila10/OneDrive - Politecnico di Milano/Documenti/PoliMi/SEL/Smart Wearables/Debug_Narwhal/USB_Middlewares" -I"C:/Users/ila10/OneDrive - Politecnico di Milano/Documenti/PoliMi/SEL/Smart Wearables/Debug_Narwhal/USB_Middlewares/ST/STM32_USB_Device_Library/Class/CDC/Inc" -I"C:/Users/ila10/OneDrive - Politecnico di Milano/Documenti/PoliMi/SEL/Smart Wearables/Debug_Narwhal/USB_Middlewares/ST/STM32_USB_Device_Library/Core/Inc" -I"C:/Users/ila10/OneDrive - Politecnico di Milano/Documenti/PoliMi/SEL/Smart Wearables/Debug_Narwhal/USB_Device/Target" -I"C:/Users/ila10/OneDrive - Politecnico di Milano/Documenti/PoliMi/SEL/Smart Wearables/Debug_Narwhal/USB_Device/App" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/AS7331.cyclo ./Core/Src/AS7331.d ./Core/Src/AS7331.o ./Core/Src/AS7331.su ./Core/Src/AS7341.cyclo ./Core/Src/AS7341.d ./Core/Src/AS7341.o ./Core/Src/AS7341.su ./Core/Src/Bluetooth.cyclo ./Core/Src/Bluetooth.d ./Core/Src/Bluetooth.o ./Core/Src/Bluetooth.su ./Core/Src/DPS310XTSA1.cyclo ./Core/Src/DPS310XTSA1.d ./Core/Src/DPS310XTSA1.o ./Core/Src/DPS310XTSA1.su ./Core/Src/IIS2MDC.cyclo ./Core/Src/IIS2MDC.d ./Core/Src/IIS2MDC.o ./Core/Src/IIS2MDC.su ./Core/Src/LSM6DSO16IS.cyclo ./Core/Src/LSM6DSO16IS.d ./Core/Src/LSM6DSO16IS.o ./Core/Src/LSM6DSO16IS.su ./Core/Src/LSM6DSV16BX.cyclo ./Core/Src/LSM6DSV16BX.d ./Core/Src/LSM6DSV16BX.o ./Core/Src/LSM6DSV16BX.su ./Core/Src/MAX30101.cyclo ./Core/Src/MAX30101.d ./Core/Src/MAX30101.o ./Core/Src/MAX30101.su ./Core/Src/MAX30205.cyclo ./Core/Src/MAX30205.d ./Core/Src/MAX30205.o ./Core/Src/MAX30205.su ./Core/Src/SPI_DMA_NAND.cyclo ./Core/Src/SPI_DMA_NAND.d ./Core/Src/SPI_DMA_NAND.o ./Core/Src/SPI_DMA_NAND.su ./Core/Src/SPI_NAND.cyclo ./Core/Src/SPI_NAND.d ./Core/Src/SPI_NAND.o ./Core/Src/SPI_NAND.su ./Core/Src/main.cyclo ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/main.su ./Core/Src/peripheral_tests.cyclo ./Core/Src/peripheral_tests.d ./Core/Src/peripheral_tests.o ./Core/Src/peripheral_tests.su ./Core/Src/stm32u5xx_hal_msp.cyclo ./Core/Src/stm32u5xx_hal_msp.d ./Core/Src/stm32u5xx_hal_msp.o ./Core/Src/stm32u5xx_hal_msp.su ./Core/Src/stm32u5xx_it.cyclo ./Core/Src/stm32u5xx_it.d ./Core/Src/stm32u5xx_it.o ./Core/Src/stm32u5xx_it.su ./Core/Src/syscalls.cyclo ./Core/Src/syscalls.d ./Core/Src/syscalls.o ./Core/Src/syscalls.su ./Core/Src/sysmem.cyclo ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/sysmem.su ./Core/Src/system_stm32u5xx.cyclo ./Core/Src/system_stm32u5xx.d ./Core/Src/system_stm32u5xx.o ./Core/Src/system_stm32u5xx.su

.PHONY: clean-Core-2f-Src

