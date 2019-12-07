from machine import I2C, Pin
import DS3231

class ConfTime(object):

	def __init__(self, sda, scl):
		self.i2c = I2C(sda = Pin(sda), scl=Pin(scl))
		self.rtc = DS3231.DS3231(self.i2c)
		
	def set_date_time(self, my_date_time):
		self.rtc.DateTime(my_date_time)

	def get_date_time(self):
		return self.rtc.DateTime()


# "Follow your Bliss" - Joseph Campbell