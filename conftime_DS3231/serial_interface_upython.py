# -*- coding: utf-8 -*-

import time
from time import sleep
import serial
import re

class SerialInterface(object):
	def __init__(self,port, baud):
		self.port = port
		self.baud = baud

	def connect_to_serial(self):
	    # print ('Opening serial port...')
	    self.serial_connection = serial.Serial(self.port, self.baud)
	    if self.serial_connection.isOpen():
	        # print ('port opened!\n')
	        return(True)
	    else:
	        return(False)

	def close_serial(self):
	    self.serial_connection.close()

	def clean_file_sys(self):
		self.repl("import os",0.1)
		files = self.repl("os.listdir()", 0.4)[2]
		files = files.decode()
		files = files.strip('[]')
		files = files.split(',')
		for i in range(len(files)):
			files[i] = files[i].replace('\'','')
			files[i] = files[i].strip(' ')
		for file in files[:]:
			if file != 'boot.py':
				self.repl("os.remove('"+file+"')",0.4)

	def repl(self, LINE, sleep_time):
	    response = ''
	    response = response.encode()
	    self.serial_connection.flushInput()
	    LINE = LINE.replace("\r", r'\r')
	    LINE = "\r" + LINE + "\r"
	    LINE = LINE.encode()
	    self.serial_connection.write(LINE)
	    sleep(sleep_time)
	    # print(self.serial_connection.inWaiting())
	    while (self.serial_connection.inWaiting() > 0):
	        response = response + self.serial_connection.read(self.serial_connection.inWaiting())
	        # print (response)
	        response = re.sub('\r'.encode(), ''.encode(), response)
	        sleep(sleep_time)
	    response_list = response.split("\n".encode())
	    return response_list
		
