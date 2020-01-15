from ble_temperature_central import BLETemperatureCentral
import bluetooth

class DOUBLE_cellphone(object):

	def __init__(self):
		self.ble = bluetooth.BLE()
		self.central_scanner = BLETemperatureCentral(self.ble)
		self.flag_not_found = False
		self.central_scanner.scan(callback=self.on_scan_callback)


	def on_scan_callback(self, addr_type, addr, name):
		if addr_type is not None:
			self.central_scanner.connect()
		else:
			self.flag_not_found = True

	def check_connectivity(self):
		return self.central_scanner.is_connected()

	def read_value(self):
		return self.central_scanner.value()

	def issue_reading(self):
		self.central_scanner.read(None)

	def deinit(self):
		self.ble.gap_scan(None)
		self.ble.active(False)

