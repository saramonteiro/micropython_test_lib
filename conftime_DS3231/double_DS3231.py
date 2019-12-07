import machine 

FREQUENCY_SCL     = (400000)
DS3231_I2C_ADDR   = (0x68)
DS3231_REG_SEC    = (0x00)
DS3231_REG_MIN    = (0x01)
DS3231_REG_HOUR   = (0x02)
DS3231_REG_WEEKDAY= (0x03)
DS3231_REG_DAY    = (0x04)
DS3231_REG_MONTH  = (0x05)
DS3231_REG_YEAR   = (0x06)

class DOUBLE_DS3231(object):
	def __init__(self, sda, scl):
		self.sda_pin = sda
		self.scl_pin = scl
		self.i2c = machine.I2C(id = 1, mode=machine.I2C.SLAVE, speed=FREQUENCY_SCL, sda=self.sda_pin,  scl=self.scl_pin, slave_addr=DS3231_I2C_ADDR)

	def DecToHex(self, dat):
		return (dat//10) * 16 + (dat%10)

	# When using this method the other methods such as Year(x), Hour(x) and the others 
	# don't have the power to update the values, since the registers is mirroring the internal rtc value
	# So, the former way it's called dynamic set and the latter static set 
	def use_internal_rtc(self,current_datetime=None):
		self.internal_rtc = machine.RTC()
		if current_datetime != None:
			self.set_current_time(current_datetime)
		else:
			current_datetime = (self.Year(), self.Month(), self.Day(), self.Hour(), self.Minute(), self.Second())
			self.set_current_time(current_datetime)
		self.my_timer = machine.Timer(1)
		self.my_timer.init(period=1000,mode=self.my_timer.PERIODIC, callback=self.my_callback)

	def set_current_time(self, current_datetime):
		self.internal_rtc.init(current_datetime)

	def HexToDec(self, dat):
		return (dat//16) * 10 + (dat%16)

	def my_callback(self,timer):
		self.current_datetime = self.internal_rtc.now()
		self.i2c.setdata(chr(self.DecToHex(self.current_datetime[0]%100)), DS3231_REG_YEAR)
		self.i2c.setdata(chr(self.DecToHex(self.current_datetime[1])), DS3231_REG_MONTH)
		self.i2c.setdata(chr(self.DecToHex(self.current_datetime[2])), DS3231_REG_DAY)
		self.i2c.setdata(chr(self.DecToHex(self.current_datetime[3])), DS3231_REG_HOUR)
		self.i2c.setdata(chr(self.DecToHex(self.current_datetime[4])), DS3231_REG_MIN)
		self.i2c.setdata(chr(self.DecToHex(self.current_datetime[5])), DS3231_REG_SEC)	
		#self.i2c.setdata(chr(self.DecToHex(self.current_datetime[6])), DS3231_REG_WEEKDAY)	


	def Second(self, second = None):
		if second == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_SEC, 1)))
		else:
			self.i2c.setdata(chr(self.DecToHex(second)), DS3231_REG_SEC)

	def Minute(self, minute = None):
		if minute == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_MIN, 1)))
		else:
			self.i2c.setdata(chr(self.DecToHex(minute)), DS3231_REG_MIN)

	def Hour(self, hour = None):
		if hour == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_HOUR, 1)))
		else:
			self.i2c.setdata(chr(self.DecToHex(hour)), DS3231_REG_HOUR)

	def Time(self, dat = None):
		if dat == None:
			return [self.Hour(), self.Minute(), self.Second()]
		else:
			self.Hour(dat[0])
			self.Minute(dat[1])
			self.Second(dat[2])

	def Weekday(self, weekday = None):
		if weekday == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_WEEKDAY, 1)))
		else:
			self.i2c.setdata(chr(self.DecToHex(weekday)), DS3231_REG_WEEKDAY)

	def Day(self, day = None):
		if day == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_DAY, 1)))
		else:
			self.i2c.setdata(chr(self.DecToHex(day)), DS3231_REG_DAY)

	def Month(self, month = None):
		if month == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_MONTH, 1)))
		else:
			self.i2c.setdata(chr(self.DecToHex(month)), DS3231_REG_MONTH)

	def Year(self, year = None):
		if year == None:
			return self.HexToDec(ord(self.i2c.getdata(DS3231_REG_YEAR, 1)))+2000
		else:
			self.i2c.setdata(chr(self.DecToHex(year%100)), DS3231_REG_YEAR)

	def Date(self, dat = None):
		if dat == None:
			return [self.Year(), self.Month(), self.Day()]
		else:
			self.Year(dat[0])
			self.Month(dat[1])
			self.Day(dat[2])

	def DateTime(self, dat = None):
		if dat == None:
			return self.Date() + [self.Weekday()] + self.Time()
		else:
			self.Year(dat[0])
			self.Month(dat[1])
			self.Day(dat[2])
			self.Weekday(dat[3])
			self.Hour(dat[4])
			self.Minute(dat[5])
			self.Second(dat[6])

	def deinit(self):
		self.i2c.deinit()
		if hasattr(self, 'my_timer'):
			self.my_timer.deinit()


