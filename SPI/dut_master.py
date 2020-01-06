from machine import Pin, SPI

class Dut_master(object):
	def __init__(self, mosi, miso, sclk, cs):
		spi_master = SPI(1, baudrate=2000000,polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(sclk), mosi=Pin(mosi), miso=Pin(miso))
		self.cs = Pin(cs, Pin.OUT)
		self.cs.on();
