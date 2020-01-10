README.TXT

This is an extra module for micropython that intended to expose the spi slave driver basic functionality for esp32. 


After too many tests this module was considered unstable, the author tested with and without DMA, with and without Tasks and the spi slave driver has been shown to be unstable in all conditions. The esp-idf version used was v 3. The micropython version used was v 1.11.

To embed the module into the firmware it was used the following command to build the firmware:
make USER_C_MODULES=../../../mymodules CFLAGS_EXTRA=-DMODULE_SPI_SLAVE_ENABLED=1 all PYTHON=python2
Considering that micropython directory was syde by syde in relation to mymodules directory.

--micropython/
--mymodules/

The command was run in the ports/esp32/ directory.

To use this module from inside the repl in the esp32:

import spi_slave

This module offers the following API:


-> spi_slave.init(mosi_pin, miso_pin, sclk_pin, cs_pin)

	This function initializes the spi bus in the slave side according with the params given. The params are int numbers, they are all proper initialized inside the function. 
	This function returns false for fail or true for success.


-> spi_slave.free_bus()

	This function deinitializes the bus, allowing others slaves to communicate to the master. It returns false for fail and true for success.

-> spi_slave.enable_transaction(list)

	This function let a transaction prepared for when the master starts a transaction. So the param is a list containing all the elements to be placed at the send buffer. For example: spi_slave.enable_transaction([1,2,3]). This is currently a blocking function, that means it will only release the repl when the transaction gets over, and it returns false for fail and returns the received buffer in the a bytearray format in the case of success. 

-> spi_slave.get_received_buffer()
	
	This function return the last transaction received buffer (bytearray format).