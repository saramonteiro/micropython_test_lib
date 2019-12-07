from machine import Pin
import time

class Led(object):

	def __init__(self, input_pin, pulses):
		self.input_pin = input_pin
		self.pulses = pulses
		self.counter = 0
		self.frequency = 0
		self.acumulator = 0
		self.periods = []
		self.start = 0
		# setup input pin
		self.pin = Pin(self.input_pin,Pin.IN, Pin.PULL_DOWN)

	def start_acquisition(self):
		# Enables digital input interruption
		self.pin.irq(trigger = Pin.IRQ_RISING, handler = self.ISR)  

	# Calculate the average frequency
	def calculate_average_frequency(self):
		self.frequency = 1/(self.calculate_average_period()/1000)

	# Calculate the average period
	def calculate_average_period(self):
		self.period =  self.acumulator/(self.pulses-1)
		return self.period

	def get_average_frequency(self):
		return self.frequency

	def get_average_period(self):
		return self.period

	def show_me_periods(self):
		print(self.periods)

	# Interrupt Service Routine 
	def ISR(self,arg):
		if(self.counter < self.pulses):
			period = time.ticks_diff(time.ticks_ms(), self.start)
			self.start = time.ticks_ms()
			if(self.counter != 0):
				self.periods.append(period)
				self.acumulator += period
			self.counter+=1
			if(self.counter == self.pulses):
				self.calculate_average_period()
				self.disable_irq()
	
	# method to be improved 
	def disable_irq(self):
		self.pin.irq(trigger=0,handler=self.ISR)

