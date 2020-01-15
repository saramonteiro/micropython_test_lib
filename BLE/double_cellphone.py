from ble_temperature_central import BLETemperatureCentral
import bluetooth

class DOUBLE_cellphone(object):

	def __init__(self):
		self.ble = bluetooth.BLE()
		central_scanner = BLETemperatureCentral(self.ble)
		self.flag_not_found = False
		self.advertising_data = []
		central_scanner.scan(callback=self.on_scan_callback)


	def on_scan_callback(self, addr_type, addr, name):
		if addr_type is not None:
			self.advertising_data = addr_type, addr, name
		else:
			self.flag_not_found = True
	
	def get_advertised_name(self):
		if self.flag_not_found == False:
			return self.advertising_data[2]
		else:
			return False

	def deinit(self):
		self.ble.gap_scan(None)
		self.ble.active(False)

