# Smart Wearable Sensor Bio

This repository contains selected hardware, firmware, software, and documentation files from a **Smart Wearables Design and Prototyping group project**.

The project aimed to develop a wearable biomedical sensing system based on eyeglasses, combining a sensor probe, STM32-based embedded firmware, data logging, data download, and basic visualization/processing.

## Important Note

This was a **group project** and not every part of the repository was developed entirely from scratch by me.

Some parts were based on the provided course/professor starter project, while other parts were completed, modified, integrated, or extended by the team. This repository is intended to document the project work and the parts uploaded for demonstration, study, and portfolio purposes.

## Project Overview

The system was designed to acquire and process wearable sensor data, including:

- IMU data from the main board
- PPG data from the MAX30101 sensor
- Temperature data from the MAX30205 sensor
- Logged data from memory
- Downloaded and decoded data using Python tools
- Optional app/user-interface related material

The complete project included both hardware and firmware/software components.

## Repository Structure

- `hardware/altium-pcb/`  
  Altium Designer PCB and schematic files for the bio-sensor probe hardware.

- `firmware/mainboard-imu-logger/`  
  STM32 firmware project related to sensor acquisition, logging, and communication.

- `firmware/debug-mainboard-and-probes/`  
  Firmware/debug project files used for testing the main board and probe communication.

- `software/imu-logger-python/`  
  Python-side tools for downloading, decoding, processing, and visualizing logged sensor data.

- `app/smart-wearables-app/`  
  App/interface-related project files.

- `docs/`  
  Documentation and user guide material.

## Hardware Design

The hardware section contains the Altium project for the bio-sensor probe.

The design includes:

- PCB layout
- Schematic design
- PCB component library
- Schematic library
- Bill of Materials document
- Output job configuration

The probe was designed around biomedical sensors such as:

- MAX30101 PPG sensor
- MAX30205 temperature sensor

## Firmware and Software

The firmware/software part includes STM32-based project files and supporting tools.

Main activities included:

- Sensor configuration
- IMU data acquisition
- PPG and temperature sensor integration
- NAND/memory logging
- USB/UART communication
- Data download
- Python decoding and visualization
- Basic signal processing for sensor data

Some firmware structure and base functionality were provided as part of the course project, while the team worked on integration, extension, debugging, and testing.

## Technologies and Tools

- STM32 / STM32CubeIDE
- C / Embedded C
- Python
- Altium Designer
- MAX30101 PPG sensor
- MAX30205 temperature sensor
- IMU sensor
- UART / USB communication
- Memory logging
- Data processing and visualization

## Disclaimer

This repository is mainly for academic and portfolio documentation. The system is a prototype developed for a university project and is not intended for medical use or clinical measurements.

## Author

Mobin Khatib  
MSc Electronics Engineering  
Politecnico di Milano
