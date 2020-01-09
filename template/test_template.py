# Do the serial interface between PC and DUT or DOUBLE
from serial_interface_upython import SerialInterface
# Library for testing with different asserts
from should_dsl import should
# Test class from wich our class inhereints
import unittest
# Operational System Interface
import os
import sys
# Utils
import time
from time import sleep

production_code = "dut_template.py"
double_code = "double_template.py"
build = "python -m mpy_cross -s -march=xtensa "
DUT_PORT = "/dev/ttyUSB0"
DOUBLE_PORT = "/dev/ttyUSB1"
send = "ampy --port "
# From set-up:
# Building, connection and sending phase
try:
	print("Building production code...")
	os.system(build+production_code)
	print("Building double code...")
	os.system(build+double_code)
	print("Cleaning the filesystem...")
	dut_serial = SerialInterface(DUT_PORT, 115200)
	dut_serial.connect_to_serial()
	dut_serial.clean_file_sys()
	dut_serial.close_serial()
	double_serial = SerialInterface(DOUBLE_PORT, 115200)
	double_serial.connect_to_serial()
	double_serial.clean_file_sys()
	double_serial.close_serial()
	print("Sending built production code...")
	os.system(send+DUT_PORT+" put "+production_code.replace(".py",".mpy"))
	print("Sending built double code...")
	os.system(send+DOUBLE_PORT+" put "+double_code.replace(".py",".mpy"))
except:
	sys.exit('fail to upload file(s)')
# Uncomment the next line for not to run the Test
# sys.exit()

# Testing Phase
class Test_Template(unittest.TestCase):
	#Creates a serial connection and import the classes
	def setUp(self):
		print('\n')
		print("Connecting to DUT device...")
		self.dut_serial = SerialInterface(DUT_PORT, 115200)
		self.dut_serial.connect_to_serial()
		print("Connecting to DOUBLE device...")
		self.double_serial = SerialInterface(DOUBLE_PORT, 115200)
		self.double_serial.connect_to_serial()
		self.dut_serial.repl("from dut_template import Dut_class", 0.1) 
		self.double_serial.repl("from double_template import Double_class", 0.1) 

	# < Space for the test cases >

	#closes serial 
	def tearDown(self):
		self.dut_serial.repl("del Dut_class", 0.2)
		self.double_serial.repl("del Double_class", 0.2)
		self.dut_serial.close_serial()
		self.double_serial.close_serial()

if __name__ == '__main__':
    unittest.main()
