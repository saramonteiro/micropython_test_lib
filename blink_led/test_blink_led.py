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

production_code = "dut_blink.py"
double_code = "double_led.py"
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
class Test_Blinker(unittest.TestCase):
	#Creates a serial connection and import the classes
	def setUp(self):
		print('\n')
		print("Connecting to DUT device...")
		self.dut_serial = SerialInterface(DUT_PORT, 115200)
		self.dut_serial.connect_to_serial()
		print("Connecting to DOUBLE device...")
		self.double_serial = SerialInterface(DOUBLE_PORT, 115200)
		self.double_serial.connect_to_serial()
		self.dut_serial.repl("from dut_blink import Blinker", 0.1) 
		self.double_serial.repl("from double_led import Led", 0.1) 

	def test_blink_blocking(self):
		led_pin_dut = "2"
		led_pin_double = "21"
		period_blink = "1000"
		blinking_times = "2"
		print("\nTesting blink_blocking with the following parameters: "+"period blinking: "+period_blink+"ms, blinking times: "+blinking_times+" x")
		# 1 - Objects Creation
		# Creates an object Led in the Double to be "blinked" in pin "led_pin_double" that expects to be blinked "blinking_times" - but doesn't starts the acquisition yet
		self.double_serial.repl("red_led = Led("+led_pin_double+","+blinking_times+")",0.1)
		# Creates an object Blinker in the DUT to blink in pin "led_pin_dut", with a period equals to "period_blink" for 5 times - but doesn't starts it yet
		self.dut_serial.repl("blinker = Blinker("+led_pin_dut+","+period_blink+","+blinking_times+")",0.1)
		# 2 - Input Injection
		# Puts the led to wait for external pulses
		self.double_serial.repl("red_led.start_acquisition()",0.1)
		# Calls the DUT to blink a led in the blocking mode
		self.dut_serial.repl("blinker.blink_blocking()",0.1)
		# 3 - Results gathering
		# Waits the DUT to blink the led for the established time 
		sleep((float(period_blink)*float(blinking_times))/1000.0)
		sleep(1)
		obtained_period = self.double_serial.repl("red_led.get_average_period()",0.2)[2]
		obtained_period = obtained_period.decode()
		obtained_period = float(obtained_period)
		period_blink = float(period_blink)
		print(obtained_period)
		# 4 - Assertion
		obtained_period |should| close_to (period_blink, delta = 1)
		# 5 - descomissioning
		self.dut_serial.repl("del blinker", 0.1)
		self.double_serial.repl("del red_led", 0.1)

	# Only to be tested isolated or as the last one(because it blocks while blinking, and it blinks forever)
	# def test_blink_blocking_forever(self):
	# 	led_pin_dut = "2"
	# 	led_pin_double = "21"
	# 	period_blink = "500"
	# 	blinking_times = "5"
	# 	print("\nTesting blink_blocking forever with the following parameters: "+"period blinking: "+period_blink+"ms, blinking times: "+blinking_times+" x")
	# 	# 1 - Objects Creation
	# 	# Creates an object Led in the Double to be "blinked" in pin 21 and expects 5 pulses - but doesn't starts the acquisition yet
	# 	self.double_serial.repl("red_led = Led("+led_pin_double+","+blinking_times+")",0.1)
	# 	# Creates an object Blinker in the DUT to blink in pin 2, at 1Hz for 5 times - but doesn't starts it yet
	# 	self.dut_serial.repl("blinker = Blinker("+led_pin_dut+","+period_blink+")",0.1)
	# 	# 2 - Input Injection
	# 	# Puts the led to wait for external pulses
	# 	self.double_serial.repl("red_led.start_acquisition()",0.1)
	# 	# Calls the DUT to blink a led in the blocking mode
	# 	self.dut_serial.repl("blinker.blink_blocking()",0.1)
	# 	# 3 - Results gathering
	# 	# Waits the DUT to blink the led for the established time 
	# 	sleep((float(period_blink)*float(blinking_times))/1000.0)
	# 	sleep(1)
	# 	obtained_period = self.double_serial.repl("red_led.get_average_period()",0.2)[2]
	# 	obtained_period = obtained_period.decode()
	# 	obtained_period = float(obtained_period)
	# 	period_blink = float(period_blink)
	# 	print(obtained_period)
	# 	# 4 - Assertion
	# 	obtained_period |should| close_to (period_blink, delta = 1)
	# 	# 5 - descomissioning
	# 	self.dut_serial.repl("del blinker", 0.1)
	# 	self.double_serial.repl("del red_led", 0.1)	

	def test_blink_isr(self):
		led_pin_dut = "2"
		led_pin_double = "21"
		period_blink = "2000"
		blinking_times = "2"
		print("\nTesting blink_isr with the following parameters: "+"period blinking: "+period_blink+"ms, blinking times: "+blinking_times+" x")
		# 1 - Objects Creation
		# Creates an object Led in the Double to be "blinked" in pin "led_pin_double" that expects to be blinked "blinking_times" - but doesn't starts the acquisition yet
		self.double_serial.repl("red_led = Led("+led_pin_double+","+blinking_times+")",0.1)
		# Creates an object Blinker in the DUT to blink in pin "led_pin_dut", with a period equals to "period_blink" for 5 times - but doesn't starts it yet
		self.dut_serial.repl("blinker = Blinker("+led_pin_dut+","+period_blink+","+blinking_times+")",0.1)
		# 2 - Input Injection
		# Puts the led to wait for external pulses
		self.double_serial.repl("red_led.start_acquisition()",0.1)
		# Calls the DUT to blink a led in the blocking mode
		self.dut_serial.repl("blinker.blink_timer_isr()",0.1)
		# 3 - Results gathering
		# Waits the DUT to blink the led for the established time 
		sleep((float(period_blink)*float(blinking_times))/1000.0)
		sleep(1)
		obtained_period = self.double_serial.repl("red_led.get_average_period()",0.2)[2]
		obtained_period = obtained_period.decode()
		obtained_period = float(obtained_period)
		period_blink = float(period_blink)
		print(obtained_period)
		# 4 - Assertion
		obtained_period |should| close_to (period_blink, delta = 1)
		# 5 - descomissioning
		self.dut_serial.repl("del blinker", 0.1)
		self.double_serial.repl("del red_led", 0.1)

	def test_blink_isr_forever(self):
		led_pin_dut = "2"
		led_pin_double = "21"
		period_blink = "1000"
		blinking_times = "2"
		print("\nTesting blink_isr forever with the following parameters: "+"period blinking: "+period_blink+"ms, blinking times: "+blinking_times+" x")
		# 1 - Objects Creation
		# Creates an object Led in the Double to be "blinked" in pin "led_pin_double" that expects to be blinked "blinking_times" - but doesn't starts the acquisition yet
		self.double_serial.repl("red_led = Led("+led_pin_double+","+blinking_times+")",0.1)
		# Creates an object Blinker in the DUT to blink in pin "led_pin_dut", with a period equals to "period_blink" for 5 times - but doesn't starts it yet
		self.dut_serial.repl("blinker = Blinker("+led_pin_dut+","+period_blink+")",0.1)
		# 2 - Input Injection
		# Puts the led to wait for external pulses
		self.double_serial.repl("red_led.start_acquisition()",0.1)
		# Calls the DUT to blink a led in the blocking mode
		self.dut_serial.repl("blinker.blink_timer_isr()",0.1)
		# 3 - Results gathering
		# Waits the DUT to blink the led for the established time 
		sleep((float(period_blink)*float(blinking_times))/1000.0)
		sleep(1)
		obtained_period = self.double_serial.repl("red_led.get_average_period()",0.2)[2]
		obtained_period = obtained_period.decode()
		obtained_period = float(obtained_period)
		period_blink = float(period_blink)
		print(obtained_period)
		# 4 - Assertion
		obtained_period |should| close_to (period_blink, delta = 1)
		# 5 - descomissioning
		self.dut_serial.repl("blinker.disable_isr();del blinker", 0.2)
		self.double_serial.repl("del red_led", 0.1)

	#closes serial and erase Classes
	def tearDown(self):
		self.dut_serial.repl("del Blinker", 0.2)
		self.double_serial.repl("del Led", 0.2)
		self.dut_serial.close_serial()
		self.double_serial.close_serial()

if __name__ == '__main__':
    unittest.main()
