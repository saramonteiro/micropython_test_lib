from machine import UART
from machine import Timer

class DOUBLE_GPS(object):
	GGA_MESSAGE = b"$GPGGA,141623.523,2143.963,S,04111.493,W,1,12,1.0,0.0,M,0.0,M,,*65\n"
	RMC_MESSAGE = b"$GPRMC,141623.523,A,2143.963,S,04111.493,W,,,301019,000.0,W*7B\n"
	UPDATE_RATE_1S = 'PMTK220,1000'
	
	def __init__(self, TX, RX, uart):
		self.uart = UART(uart, baudrate=9600)
		self.uart.init(9600,bits=8,tx=TX,rx=RX)
		self.flag = False

	def make_data_available(self,NMEA_sentence):
		self.uart.write(NMEA_sentence)

	def received_command(self):
		command = self.uart.readline()
		if(command != None):
			command, received_check_sum = command.split(b'*')
			command = command.strip(b'$')
			received_check_sum = received_check_sum[0:2]
			generated_check_sum = self.generate_checksum(command)
			command = command.decode()
			if command == self.UPDATE_RATE_1S:
				self.continuous_mode()
				self.flag = True
			return command
		else:
			return None

	def generate_checksum(self, command):
		checksum = 0
		for char in command:
		    checksum ^= char
		return checksum

	def continuous_mode(self):
		self.my_timer = Timer(1)
		self.my_timer.init(period=1000,mode=self.my_timer.PERIODIC, callback=self.my_callback)

	def my_callback(self,timer):
		self.make_data_available(self.RMC_MESSAGE)

	def deinit(self):
		self.uart.deinit()
		if hasattr(self, 'my_timer'):
			self.my_timer.deinit()