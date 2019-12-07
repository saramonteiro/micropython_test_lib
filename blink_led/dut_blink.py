from machine import Pin
from machine import Timer
import time

class Blinker(object):
	def __init__(self, output_pin, period, pulses = None):
		# setup output pin
		self.output_pin = output_pin
		self.period = period
		self.pulses = pulses
		self.pin = Pin(self.output_pin,Pin.OUT)
		self.pin.off()
		self.counter = 0

	# Blocks the REPL until it has finished
	def blink_blocking(self):
		if self.pulses == None:
			while True:
				self.pin.value(not self.pin.value())
				time.sleep_ms(int(self.period/2))
		else:
			for i in range(0,(self.pulses)*2):
				self.pin.value(not self.pin.value())
				time.sleep_ms(int(self.period/2))

	def callback_timer(self,arg):
		self.pin.value(not self.pin.value())
		if (self.pulses != None):
			self.counter+=1
			if(self.counter == (self.pulses*2)):
				self.timing.deinit()
				self.counter = 0 

	def disable_isr(self):
		self.pin.off()
		self.timing.deinit()

	# Uses an interruption timer and callback function to trigger the toggle
	def blink_timer_isr(self):
		self.timing = Timer(-1)
		self.timing.init(period=int(self.period/2), mode=Timer.PERIODIC, callback=self.callback_timer)


# "If I have seen further it is by standing on the shoulders of Giants." Isaac Newton
