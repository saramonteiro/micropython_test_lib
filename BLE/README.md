# BLE Demo  

This example shows how to test a BLE connection and reading on a Peripheral device. Part of it uses the temperature sensor example provided [here](https://github.com/micropython/micropython/tree/master/examples/bluetooth). 
The DUT is playing the role of a Peripheral device that is a temperature sensor. The DOUBLE plays the role of a Central device like a smartphone. The test is going to verify if the Peripheral is rightly connecting to Central devices and if it's correcting providing data when requested.

## Firmwares
DUT: [micropython original firmware](http://micropython.org/download#esp32).

DOUBLE: [micropython original firmware](http://micropython.org/download#esp32).

P.S: The BLE module is very recent and initialization time was indeterministic the last time it was tested, sometimes it causes test errors. So the results of the tests are unstable.

## How to run it:
``` 
python3 test_sensor_cellphone.py -v
``` 
Since the BLE is a wireless protocol, no wired connection is done.



