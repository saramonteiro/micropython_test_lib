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

production_code = "dut_master.py"
double_code = "double_slave.py"
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
	os.system(send+DUT_PORT+" put "+production_code)#.replace(".py",".mpy"))
	print("Sending built double code...")
	os.system(send+DOUBLE_PORT+" put "+double_code)#.replace(".py",".mpy"))
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
		self.dut_serial.repl("from dut_master import Dut_master", 0.1) 
		self.double_serial.repl("from double_slave import Double_slave", 0.1) 


	def test_reading_registers_without_indicating_address(self):
		print("\nTesting the method read_registers_wo_address()")
		expected_readings = [1,2,3]
		gotten_readings = []
		print("Expected Readings "+str(expected_readings))
		# 1 - Objects Creation
		self.double_serial.repl("slave = Double_slave(13,12,14,15)",0.2)
		self.dut_serial.repl("master = Dut_master(13,12,14,15)",0.2)
		# 2 - Input Injection
		self.double_serial.repl("slave.enable_transaction("+str(expected_readings)+")",0.2)
		# 3 - Results gathering
		gotten_readings = self.dut_serial.repl("master.read_registers_wo_address(3)",0.2)[2]
		gotten_readings = gotten_readings.decode()
		# 4 - Assertion
		print("Gotten value: "+gotten_readings)
		gotten_readings |should| equal_to (str(expected_readings))

	def test_reading_registers_indicating_address(self):
		print("\nTesting the method read_registers_w_address()")
		expected_readings = [1,2,3]
		expected_written = [14,0,0,0]
		gotten_readings = []
		print("Expected Readings "+str(expected_readings))
		# 1 - Objects Creation
		self.double_serial.repl("slave = Double_slave(13,12,14,15)",0.2)
		self.dut_serial.repl("master = Dut_master(13,12,14,15)",0.2)
		# 2 - Input Injection
		self.double_serial.repl("slave.enable_transaction([0,1,2,3])",0.2)
		# 3 - Results gathering
		gotten_readings = self.dut_serial.repl("master.read_registers_w_address(14,3)",0.2)[2]
		gotten_readings = gotten_readings.decode()
		gotten_written = self.double_serial.repl("slave.get_received_buffer()",0.2)[2]
		gotten_written = gotten_written.decode()
		# 4 - Assertion
		print("Gotten value: "+gotten_readings)
		gotten_readings |should| equal_to (str(expected_readings)) 
		gotten_written |should| equal_to (str(expected_written))

	def test_writing_registers_without_indicating_address(self):
		print("\nTesting the method write_registers_wo_address()")
		expected_written = [1,2,3]
		gotten_values = []
		print("Expected written values "+str(expected_written))
		# 1 - Objects Creation
		self.double_serial.repl("slave = Double_slave(13,12,14,15)",0.2)
		self.dut_serial.repl("master = Dut_master(13,12,14,15)",0.2)
		# 2 - Input Injection 
		self.double_serial.repl("slave.enable_transaction([0,0,0])",0.2)
		self.dut_serial.repl("master.write_registers_wo_address("+str(expected_written)+")",0.2)
		# 3 - Results gathering
		gotten_values = self.double_serial.repl("slave.get_received_buffer()", 0.2)[2]
		gotten_values = gotten_values.decode()
		# 4 - Assertion
		print("Gotten value: "+gotten_values)
		gotten_values |should| equal_to (str(expected_written))

	def test_writing_registers_indicating_address(self):
		print("\nTesting the method write_registers_w_address()")
		expected_written = [1,2,3]
		address = 14
		gotten_values = []
		print("Expected written values "+str(expected_written))
		# 1 - Objects Creation
		self.double_serial.repl("slave = Double_slave(13,12,14,15)",0.2)
		self.dut_serial.repl("master = Dut_master(13,12,14,15)",0.2)
		# 2 - Input Injection 
		self.double_serial.repl("slave.enable_transaction([0,0,0,0])",0.2)
		self.dut_serial.repl("master.write_registers_w_address("+str(address)+","+str(expected_written)+")",0.2)
		# 3 - Results gathering
		gotten_values = self.double_serial.repl("slave.get_received_buffer()",0.2)[2]
		gotten_values = gotten_values.decode()
		# 4 - Assertion
		print("Gotten value: "+gotten_values)
		expected_written.insert(0,address)
		gotten_values |should| equal_to (str(expected_written))

	#closes serial 
	def tearDown(self):
		self.dut_serial.repl("master.deinit(); del master; del Dut_master;", 0.2)
		self.double_serial.repl("slave.deinit(); del slave; del Double_slave;", 0.2)
		self.dut_serial.close_serial()
		self.double_serial.close_serial()

if __name__ == '__main__':
    unittest.main()
