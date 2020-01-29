# SPI slave mode for ESP32

The original micropython firmware does not support spi in the slave mode on esp32. So this module was created to allow developing test cases to verify
a production code that uses the SPI in the master mode. 
You can use the new functionality in two ways:
* Building your own firmware along with the extra module that is available on `mymodules/spi_slave/` dir. The instructions to build are in the next section "SPI module".
* Or you can simply get the pre-built-firmware on `pre-built-firmware/` dir. The instructions to upload it is in the next section "Pre Built Firmware with support for SPI slave mode".

## SPI Module

This is the extra module for micropython that intended to expose the spi slave driver's basic functionality for esp32. 

After too many tests this module was considered unstable, it was tested with and without DMA, with and without Tasks and the spi slave driver has been shown unstable in all conditions. The esp-IDF version used was v 3.3. The micropython version used was v 1.11.

Considering you have configured the ESP-IDF toolchain and cloned the micropython repository, to build and to embed the module into the firmware you should run the following command:

    make USER_C_MODULES=../../../mymodules CFLAGS_EXTRA=-DMODULE_SPI_SLAVE_ENABLED=1 all PYTHON=python2

Considering that the micropython directory was side by side to mymodules directory.

--micropython/

--mymodules/

The command was run in the ports/esp32/ directory.

After running this command, just run `make deploy` to upload the newly built firmware. This command uses by standard the `/dev/ttyUSB0` port. If your device is using another port, it should be passed as a parameter. The full documentation is at micropython's official repository.

To use this module from inside the repl in the esp32:

    import spi_slave

This module offers the following API:

* `spi_slave.init(mosi_pin, miso_pin, sclk_pin, cs_pin)`

    This function initializes the spi bus on the slave side according to the params given. The params are int numbers, they are all proper initialized inside the function. 
    This function returns false for failure or true for success.


* `spi_slave.free_bus()`

    This function deinitializes the bus, allowing other slaves to communicate with the master. It returns false for failure and true for success.

* `spi_slave.enable_transaction(list)`

    This function lets a transaction prepared for when the master starts a transaction. So the param is a list containing all the elements to be placed at the send buffer. For example: spi_slave.enable_transaction([1,2,3]). This is currently a blocking function, which means it will only release the repl when the transaction gets over, and it returns false for fail and returns the received buffer in a byte array format in the case of success. 

* `spi_slave.get_received_buffer()`
    
    This function returns the last transaction received buffer (byte array format).

Special thanks to Zoltán Vörös for this helpful discussion and for the most complete guide to starting building my own module:
https://github.com/v923z/micropython-usermod/issues/3
https://micropython-usermod.readthedocs.io/en/latest/usermods_01.html

## Pre Built Firmware with support for SPI slave mode

This a ready-to-use pre-built firmware with support for SPI in the slave mode. Using this module it is not necessary to build the whole firmware. You only need to use esptool to upload it. 

First erase the flash with the following command:

    esptool.py --port /dev/ttyUSB0 erase_flash

Then, after erasing, just upload the firmware with the following command:

    esptool.py --chip esp32 --port /dev/ttyUSB1 --baud 460800 write_flash -z 0x1000 firmware.bin 

P.S: make sure you have esptool installed. 
You may check if everything is ok opening the repl using picocom:
    picocom /dev/ttyUSB0 -b115200
    
    
Remember: this firmware is only for the double, the DUT remains with the original firmware.
    
## Example on how to use it

* Slave side
```python
import spi_slave;
spi_slave.init(13,12,14,15);
tx = bytearray('hi master')
tx = list(tx)
spi_slave.enable_transaction(tx)
spi_slave.get_received_buffer()
```
* Master side
```python
from machine import Pin, SPI;
spi_master = SPI(1, baudrate=1000000,polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12));
cs = Pin(15, Pin.OUT);
tx = bytearray('hi slave!')
rx = bytearray(len(tx))
cs.off()
spi_master.write_readinto(tx,rx)
cs.on()
rx #it will show the received result
```
Try it: Just paste the snippets on the repl. First the slave, after the master. Or try to run step-by-step.
