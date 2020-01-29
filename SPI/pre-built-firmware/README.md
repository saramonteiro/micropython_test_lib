# Pre built firmware with support for SPI slave

This a ready-to-use pre built firmware with support for SPI in the slave mode. Using this module it is not necessary to build the whole firmware. You only need to use esptool to upload it. 

First erase the flash with the following command:

    esptool.py --port /dev/ttyUSB0 erase_flash

Then, after erasing, just upload the firmware with the following command:

    esptool.py --chip esp32 --port /dev/ttyUSB1 --baud 460800 write_flash -z 0x1000 firmware.bin 

P.S: make sure you have esptool installed. 
Warning: This module is considered unstable. To see all the functions available on the API, see the README.md inside the module's source code directory. This module is intended to be used on the double.  
