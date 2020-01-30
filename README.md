# micropython_test_lib

This repository intends to present a method and the implementation for testing embedded micropython software using TDD (Test Driven Development) and HILS (Hardware in the loop Simulation). The tests are especially for drivers, that interact directly with external hardware. This repository contains multiple artifacts such as different test cases using different protocols (UART, I2C, GPIO, BLE, SPI) that serve as examples of how to test some drivers. It also contains utilities that made the tests possible and this guide for using all this tool.

The purposed method is drawn in the figure below:

![Test Method](https://github.com/saramonteiro/micropython_test_lib/blob/master/images/method.png)

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
  
  The first thing we have to do before running the tests is to erase the flash memory and to upload a micropython firmware. The latest micropython firmware may be downloaded from [micropython original firmwares](http://micropython.org/download#esp32). Download the latest generic idfv3 firmware.
> The DUT will use this firmware in all the test cases. However, the DOUBLE will use this firmware only on the blink_led, GPS and BLE examples. On the RTC example, it will use this another third-party firmware: [micropython with i2c slave mode](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/firmwares). On the SPI example, it will use the [micropython with spi slave mode](https://github.com/saramonteiro/micropython_test_lib/tree/master/SPI/pre-built-firmware). It has spi slave support and is part of this work.

To upload the firmware we are going to use the `esptool`. It's a tool that allows us to erase the flash memory and write the firmware on it. Set aside a directory where you will download your firmwares and install esptool to do the upload.
Inside this directory create a virtual environment:
``` 
python3 -m venv myfirmwares
``` 
Activate the virtual env with:
``` 
source myfirmwares/bin/activate
``` 
From inside it, install [esptool](https://pypi.org/project/esptool/) with:
``` 
pip install esptool 
``` 
Erase the flash specifying the port with the following command:
``` 
esptool.py --port /dev/ttyUSB0 erase_flash
```
Finally do the firmware upload with:
``` 
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-idf3-20200128-v1.12-96-gc3095b37e.bin
```
The last parameter is a binary. The firmware itself.

Ready! You may now use picocom or another serial terminal tool to enter the repl.

P.S: The I2C firmware has its own script that flashes the memory, but also uses esptool. When you download the firmware and unpack the zip, run the following command from the ep32 directory to upload the firmware: 
``` 
../flash.sh -p /dev/ttyUSB0
``` 
Always erase the flash before uploading.

# Templates

Now that you have the micropython firmware uploaded to the boards it's time to clone this project, install the dependencies and verify if everything is right. The templates have two goals: to serve as a starting point for developers to create their own tests and to verify if the dependencies were correctly installed.

First, clone this project:
``` 
git clone https://github.com/saramonteiro/micropython_test_lib.git
``` 
Open the micropython_test_lib directory and create a virtual env inside it.
``` 
python3 -m venv test-env
``` 
Activate the virtual env with:
``` 
source test-env/bin/activate
``` 
Install all the required dependencies:
``` 
pip install -r requirements.txt
``` 
Connect the esp32 boards and check the USB port each device is connected to. Enter on Templates directory, open the `test_template.py` file and modify the constants `DUT_PORT` and `DOUBLE_PORT`according to your connection. Save it. Close it. And runt it:
``` 
python3 test_template.py -v
``` 
The test_template doesn't have any test case but it will test the environment and the communication to the boards.

If everything is right, you should expect a screen like this:

![Installation ok](https://github.com/saramonteiro/micropython_test_lib/blob/master/images/ambiente_ok.png)

# Running the Examples

After checking your environment, try the examples only running the `test_*.py` files contained on the directories the same way you ran the `test_template.py`. Observe that there's a convention for the files' names. This makes it easy to identify the codes.
More detailed information about each test and the electrical connection is kept inside each directory. 

P.S: It's recommended to reset the boards before running tests.

# Troubleshooting

* If you're having problems to upload the files or if it's not injecting commands properly, the DUT or the double may have entered on raw repl mode. To check it, you may use the picocom or other terminal emulation tools. To work around this problem, and others, it's recommended to reset the boards.  This ensures there's no residual object. For problems like this, you should also check your cable and the configured USB port.  
* It's not recommended to interrupt tests since all tests have a routine of multiple steps from initialization to decommissioning. An interruption may lead to unexpected behavior. 
* This tool was designed to have all files pre-compiled before uploading, however, each firmware demands on a specific mpy-cross version. That's because many examples sent python files instead of micropython files. You may change the mpy-cross version in requirements.txt to pre-compile files for a specific firmware.
* SPI and BLE examples are unstable. The [5489 issue](https://github.com/micropython/micropython/issues/5489) reports an inconsistent init time for BLE module, which is very recent. This may cause problems during the text executions because the test relies on a deterministic time.   
* To track the commands that are sent and the results that are gathered through serial you may uncomment the line ```print (response)``` on the module ```serial_interface_upython.py```. This will help for debugging purposes.

# Future Works

It's intended to become this tool into a command-line tool where dynamic parameters, such as USB port and others may be set on the terminal instead of being directly changed on code.  
