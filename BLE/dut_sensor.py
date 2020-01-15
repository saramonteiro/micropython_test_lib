from ble_temperature import BLETemperature
import bluetooth

class BLE_Sensor(object):

	def __init__(self, name):
		self.ble = bluetooth.BLE()
		self.sensor = BLETemperature(self.ble, name)

	def set_value(self, value, notification = False):
		self.sensor.set_temperature(value, notification)

	def deinit(self):
		self.ble.gap_advertise(None)
		self.ble.active(False)
