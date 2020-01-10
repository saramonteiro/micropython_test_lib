from machine import Pin, SPI
import time

class Dut_master(object):
	def __init__(self, mosi, miso, sclk, cs):
		self.spi_master = SPI(1, baudrate=2000000,polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(sclk), mosi=Pin(mosi), miso=Pin(miso))
		self.cs = Pin(cs, Pin.OUT)
		self.cs.on();
		self.delay = 0.050

	def read_registers_wo_address(self, num_readings):
		readings = b''
		self.cs.off()
		time.sleep(self.delay)
		for i in range(0,num_readings):
			readings += self.spi_master.read(1)
			time.sleep(self.delay)
		self.cs.on()
		readings = list(readings)
		return readings

	def read_registers_w_address(self, address, num_readings):
		readings = b''
		self.cs.off()
		time.sleep(self.delay)
		self.spi_master.write(bytes([address]))
		for i in range(0,num_readings):
			time.sleep(self.delay)
			readings += self.spi_master.read(1)
		time.sleep(self.delay)
		self.cs.on()
		readings = list(readings)
		return readings

	def write_registers_wo_address(self, values):
		self.cs.off()
		time.sleep(self.delay)
		for value in values:
			self.spi_master.write(bytes([value]))
			time.sleep(self.delay)
		self.cs.on()
		return len(values)	

	def write_registers_w_address(self, address, values):
		self.cs.off()
		time.sleep(self.delay)
		self.spi_master.write(bytes([address]))
		for value in values:
			time.sleep(self.delay)
			self.spi_master.write(bytes([value]))
		time.sleep(self.delay)
		self.cs.on()
		return len(values)


	def deinit(self):
		self.spi_master.deinit()