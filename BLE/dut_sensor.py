from ble_temperature import BLETemperature
import bluetooth

class BLE_Sensor(object):

	def __init__(self, name):
		self.ble = bluetooth.BLE()
		sensor = BLETemperature(self.ble, name)

	def deinit(self):
		self.ble.gap_advertise(None)
		self.ble.active(False)