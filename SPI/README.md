# SPI slave mode for ESP32

The original micropython firmware does not support spi in the slave mode on esp32. So this module was created to allow developing test cases to verify
a production code that uses the SPI in the master mode. 
You can use the new functionality by two ways:
* Building your own firmware along with the extra module that is available on `mymodules/spi_slave/` dir. The instructions to build is in the next section "SPI module".
* Or you can simply get the pre-built-firmware on `pre-built-firmware/` dir. The instructions to upload it is in the next section "Pre Built Firmware with support for SPI slave mode".

## SPI Module

This is the extra module for micropython that intended to expose the spi slave driver basic functionality for esp32. 

After too many tests this module was considered unstable, it was tested with and without DMA, with and without Tasks and the spi slave driver has been shown to be unstable in all conditions. The esp-idf version used was v 3.3. The micropython version used was v 1.11.

Considering you have configured the ESP-IDF toolchain and cloned the micropython repository, to build an to embed the module into the firmware it was used the following command:

    make USER_C_MODULES=../../../mymodules CFLAGS_EXTRA=-DMODULE_SPI_SLAVE_ENABLED=1 all PYTHON=python2

Considering that micropython directory was syde by syde in relation to mymodules directory.

--micropython/

--mymodules/

The command was run in the ports/esp32/ directory.

After running this command, just run `make deploy` to upload the new built firmware. This command uses by standard the `/dev/ttyUSB0` port. If your device is using other port. It should be passed as parameter. The full documentation is at micropython's official repository.

To use this module from inside the repl in the esp32:

    import spi_slave

This module offers the following API:

* `spi_slave.init(mosi_pin, miso_pin, sclk_pin, cs_pin)`

	This function initializes the spi bus in the slave side according with the params given. The params are int numbers, they are all proper initialized inside the function. 
	This function returns false for fail or true for success.


* `spi_slave.free_bus()`

	This function deinitializes the bus, allowing others slaves to communicate to the master. It returns false for fail and true for success.

* `spi_slave.enable_transaction(list)`

	This function let a transaction prepared for when the master starts a transaction. So the param is a list containing all the elements to be placed at the send buffer. For example: spi_slave.enable_transaction([1,2,3]). This is currently a blocking function, that means it will only release the repl when the transaction gets over, and it returns false for fail and returns the received buffer in the a bytearray format in the case of success. 

* `spi_slave.get_received_buffer()`
	
	This function return the last transaction received buffer (bytearray format).

Special thanks to Zoltán Vörös for this helful discussion and for the most complete guide to start building my own module:
https://github.com/v923z/micropython-usermod/issues/3
https://micropython-usermod.readthedocs.io/en/latest/usermods_01.html

## Pre Built Firmware with support for SPI slave mode
