# micropython_test_lib

This repository intends to present a method and the implementation for testing embedded micropython software using TDD (Test Driven Development) and HILS (Hardware in the loop Simulation). The tests are especially for drivers, that interact directly with external hardware. This repository contains multiple artifacts such as different test cases using different protocols (UART, I2C, GPIO, BLE, SPI) that serve as examples of how to test some drivers. It also contains utilities that made the tests possible and this guide for using all this tool.

The purposed method is drawn in the figure below:

![Test Method](https://github.com/saramonteiro/micropython_test_lib/blob/master/method.png)

The test architecture is compounded of 3 devices and
3 codes: 
* **Devices**:
  * **1 Computer**: hosts the test application and responsible for the test execution.
  * **2 microcontrollers (both are esp32)**: 
    * **DUT (Device Under Test)**: hosts the production code that is the test’s target.
    * **DOUBLE**: another microcontroller that hosts the double code that plays the role of a (real) external peripheral, for example a RTC, a GPS, and even a simple led. The double provides inputs to the device under test and receives outputs from it, making the doubled devices transparent from the device under test’s viewpoint.
* **Codes**:
  *  **Test Code**: The test code is on the PC. It orchestrates the test, communicates to each device injecting commands and gathers results. Following the TDD philosophy, this software must be written before the production code. 
  *  **Double Code**: It's embedded on the DOUBLE. Its role is to pretend to be an external peripheral. During the development of this tool, some functional doubles were created. But It's expected that the community and the peripheral manufacturers produce their double code and make it available for test and development. 
  *  **Production Code**: It's the code we want to test!
  
# Setting up the environment

1. **Micropython firmware**
  The first thing we have to do before running the tests is to erase the flash memory and to upload a micropython firmware.The latest micropython firmware may be downloaded from [micropython original firmwares](http://micropython.org/download#esp32). Download the latest generic idfv3 firmware.
> The DUT will use this firmware in all the test cases. However, the DOUBLE will use this only the blink_led, GPS and BLE examples. On the RTC example, it will use this another third-party firmware: [micropython with i2c slave mode](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/firmwares). On the SPI example it will the [micropython with spi slave mode](https://github.com/saramonteiro/micropython_test_lib/tree/master/SPI/pre-built-firmware) has spi slave support and is part of this work.

# Templates

# Running the Examples

# SPI Slave Module

# Troubleshooting

* If you're having problems to upload the files or if it's not injecting commands properly, the DUT or the double may have entered on raw repl mode. To check it, you may use the picocom or ohter terminal emulation tool. To work around this problem, and others, it's recommended to reset the boards.  This ensures there's no residual object. For problems like this, you should also check your cable and the configured USB port.  
* It's not recommended to interrupt tests since all tests have a routine of multiple steps from initialization to decommissioning. An interruption may lead to unexpected behavior. 
* This tool was designed to have all files pre-compiled before uploading, however, each firmware demands on a specific mpy-cross version. That's because many examples sent python files instead of micropython files. You may change the mpy-cross version in requirements.txt to pre-compile files for a specific firmware.
* SPI and BLE examples are unstable. The [5489 issue](https://github.com/micropython/micropython/issues/5489) reports an inconsistent init time for BLE module, that is very recent. This may cause problems during the text executions because the test relies on a deterministic time.   
* To track the commands that are sent and the results that are gathered through serial you may uncomment the line ```print (response)``` on the module ```serial_interface_upython.py```. This will help for debugging purposes.

# Future Works

It's intended to become this tool into a command line tool where dynamic parameters, such as USB port and others may be set on the terminal instead of being directly changed on code.  
