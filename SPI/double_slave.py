import spi_slave

class Double_slave(object):
	def __init__(self, mosi, miso, sclk, cs):
		spi_slave.init(mosi,miso,sclk,cs);
		self.modes = {'READ_WO_REG':1, 'WRITE_WO_REG':2, 'READ_W_REG':3, 'WRITE_W_REG':4 }

	def set_memory_registers(self, reg_address, values):
		return spi_slave.write_on_registers(reg_address, values)

	def get_memory_registers(self, reg_address, num_values):
		return list(spi_slave.read_registers(reg_address, num_values))

	def enable_transfers(self, mode, num_transfers):
		case = self.modes.get(mode, False)
		if case == False:
			return False
		else:
			return spi_slave.enable_transfers(case, num_transfers)

	def set_register_address(self, reg_address):
		return spi_slave.set_register_pointer(reg_address)

	def disable_transfers(self):
		return spi_slave.disable_transfers()

	def deinit(self):
		return spi_slave.free_bus()

