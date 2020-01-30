# GPS Demo - UART 

This example shows how to test a UART driver. For this purpose, the DOUBLE plays the role of a GPS peripheral. Besides the test, it also can be very useful when the GPS signal is out and you need to get a fake NMEA sentence.
There are two tests. The one that ends with "itself" uses a second UART from the DUT to simulate the GPS and doesn't use another board as DOUBLE. This means that in the absence of another esp32 you may use only one board depending on what you want to test,

## Firmwares
DUT: [micropython original firmware](http://micropython.org/download#esp32).

DOUBLE: [micropython original firmware](http://micropython.org/download#esp32).

## How to run it:
``` 
python3 test_positioning_GPS.py -v
``` 

## Electrical Connections

| DUT | |  DOUBLE |  |
---- | ---- | ---- | ----
RX | TX | RX | TX
16 | 17 | 16 | 22



