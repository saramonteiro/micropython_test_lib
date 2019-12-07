from machine import UART
import utime as time
from adafruit_gps import GPS

class Positioning(object):
	def __init__(self, TX, RX, uart):
		self.uart = UART(uart, baudrate=9600)
		self.uart.init(9600,bits=8,tx=TX,rx=RX)
		self.gps = GPS(self.uart)

	def send_command(self, command):
		self.gps.send_command(command)

	def received_command(self):
		command = self.uart.readline()
		if(command != None):
			return command
		else:
			return None

	def get_latitude(self):
		self.gps.update()
		return self.gps.latitude

	def deinit(self):
		self.uart.deinit()

# "Difficulties make ordinary people become extraordinary-people" - 
