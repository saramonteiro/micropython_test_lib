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

production_code = "dut_sensor.py"
double_code = "double_cellphone.py"
auxiliary_double_codes = ["ble_advertising.py", "ble_temperature_central.py"]
auxiliary_dut_codes = ["ble_advertising.py", "ble_temperature.py"]
build = "python -m mpy_cross -s -march=xtensa "
DUT_PORT = "/dev/ttyUSB1"
DOUBLE_PORT = "/dev/ttyUSB2"
send = "ampy --port "
# From set-up:
# Building, connection and sending phase
# try:
# 	print("Building production code...")
# 	os.system(build+production_code)
# 	print("Building double code...")
# 	os.system(build+double_code)
# 	print("Cleaning the filesystem...")
# 	dut_serial = SerialInterface(DUT_PORT, 115200)
# 	dut_serial.connect_to_serial()
# 	dut_serial.clean_file_sys()
# 	dut_serial.close_serial()
# 	double_serial = SerialInterface(DOUBLE_PORT, 115200)
# 	double_serial.connect_to_serial()
# 	double_serial.clean_file_sys()
# 	double_serial.close_serial()
# 	print("Sending built production code...")
# 	os.system(send+DUT_PORT+" put "+production_code)#.replace(".py",".mpy"))
# 	print("Sending auxiliary production codes...")
# 	for code in auxiliary_dut_codes:
# 		os.system(send+DUT_PORT+" put "+code)
# 	print("Sending built double code...")
# 	os.system(send+DOUBLE_PORT+" put "+double_code)#.replace(".py",".mpy"))
# 	print("Sending auxiliary double codes...")
# 	for code in auxiliary_double_codes:
# 		os.system(send+DOUBLE_PORT+" put "+code)
# except:
# 	sys.exit('fail to upload file(s)')
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
		self.dut_serial.repl("from dut_sensor import BLE_Sensor", 0.1) 
		self.double_serial.repl("from double_cellphone import DOUBLE_cellphone", 0.1) 

	def test_advertising(self):
		print("Testing if the dut is correctly advertising itself")
		advertising_name = "my_sensor"
		# 1, 2 - Objects Creation and Input Injection
		self.dut_serial.repl("sensor = BLE_Sensor(\""+advertising_name+"\")", 0.1)
		self.double_serial.repl("cellphone = DOUBLE_cellphone()", 0.1)
		# An interval for the peripheral to start advertising
		# and for the central to start scanning and get the peripheral data 
		time.sleep(5)
		# 3 - Result Gathering
		gotten_name = self.double_serial.repl("cellphone.get_advertised_name()", 0.2)
		print(gotten_name)
		gotten_name = gotten_name[2]
		gotten_name = gotten_name.decode()
		print(gotten_name)
		print("Gotten name:", gotten_name, "  Configured name", advertising_name)
		gotten_name |should| contain (advertising_name)

	#closes serial 
	def tearDown(self):
		self.dut_serial.repl("sensor.deinit();del sensor ;del BLE_Sensor", 0.2)
		self.double_serial.repl("cellphone.deinit();del cellphone;del DOUBLE_cellphone", 0.2)
		self.dut_serial.close_serial()
		self.double_serial.close_serial()

if __name__ == '__main__':
    unittest.main()
