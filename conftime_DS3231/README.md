# DS3231 Demo - I2C
This example shows how to test a I2C driver. The DOUBLE plays the role of the RTC DS3231. The test will verify if the DUT is correctly setting and getting datetime info. The DOUBLE uses an internal timer to simulate the RTC behavior. It is transparent, so if you replace a true RTC by the DOUBLE with a predefined datetime, the DUT will continue reading as if it was reading from a real RTC. 

## Firmwares
DUT: [micropython original firmware](http://micropython.org/download#esp32).

DOUBLE: [micropython with i2c slave mode](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/firmwares).

## How to run it:
``` 
python3 test_conftime_DS3231.py -v
``` 

## Electrical Connections

|| DUT | DOUBLE
---- | ---- | ---- 
SDA | 21 | 21
SCL | 22 | 22


It's necessary to use one pull-up resistor in each bus. It was used 4,7K ohms during the tests.
