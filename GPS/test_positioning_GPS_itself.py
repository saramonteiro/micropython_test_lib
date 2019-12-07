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

production_code = "dut_positioning.py"
double_code = "double_GPS.py"
auxiliar_code = "adafruit_gps.py"
build = "python -m mpy_cross -s -march=xtensa "
DUT_PORT = "/dev/ttyUSB0"
send = "ampy --port "
# From set-up:
# Building, connection and sending phase
try:
	print("Building production code...")
	os.system(build+production_code)
	print("Building double code...")
	os.system(build+double_code)
	print("Building auxiliar code...")
	os.system(build+auxiliar_code)
	print("Cleaning the filesystem...")
	dut_serial = SerialInterface(DUT_PORT, 115200)
	dut_serial.connect_to_serial()
	dut_serial.clean_file_sys()
	dut_serial.close_serial()
	print("Sending built production code...")
	os.system(send+DUT_PORT+" put "+production_code.replace(".py",".mpy"))
	print("Sending built auxiliar_code...")
	os.system(send+DUT_PORT+" put "+auxiliar_code.replace(".py",".mpy"))
	print("Sending built double code...")
	os.system(send+DUT_PORT+" put "+double_code.replace(".py",".mpy"))
except:
	sys.exit('fail in set-up phase')
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
		self.dut_serial.repl("from dut_positioning import Positioning", 0.1) 
		self.dut_serial.repl("from double_GPS import DOUBLE_GPS", 0.1) 

	def test_send_command_itself(self):
		print("\nTesting the method send_command()")
		expected_command = 'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
		print("Expected command: "+expected_command)
		# 1 - Objects Creation
		self.dut_serial.repl("gps = DOUBLE_GPS(17,16,2)",0.2)
		self.dut_serial.repl("tracker = Positioning(23,22,1)",0.2)
		# 2 - Input Injection
		self.dut_serial.repl("tracker.send_command('"+expected_command+"')", 0.2)
		# 3 - Results gathering
		gotten_datetime = self.dut_serial.repl("gps.received_command()",0.2)[2]
		# 4 - Assertion
		gotten_datetime = gotten_datetime.decode() 
		gotten_datetime = gotten_datetime.replace('\'','')
		print("Gotten command: "+gotten_datetime)
		gotten_datetime |should| equal_to (expected_command)

	#Closes serial 
	def tearDown(self):
		# 5 Descomissioning
		self.dut_serial.repl("gps.deinit(); del gps",0.2)[2]
		self.dut_serial.repl("tracker.deinit(); del tracker",0.2)[2]
		self.dut_serial.close_serial()

if __name__ == '__main__':
    unittest.main()
