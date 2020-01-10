import spi_slave

class Double_slave(object):
	def __init__(self, mosi, miso, sclk, cs):
		spi_slave.init(mosi,miso,sclk,cs);

	def enable_transaction(self, send_buffer):
		return spi_slave.enable_transaction(send_buffer)

	def get_received_buffer(self):
		return list(spi_slave.get_received_buffer())

	def deinit(self):
		return spi_slave.free_bus()

