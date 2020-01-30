# Blink Led Demo

When we start programming in microcontrollers, the most basic code we do is a blink led. It's a "hello world" for microcontroller!
So, the first example here also tests a production code which blinks a led. The double here is playing the role of a led.

## Firmwares
DUT: [micropython original firmware](http://micropython.org/download#esp32).

DOUBLE: [micropython original firmware](http://micropython.org/download#esp32).

## How to run it:
``` 
python3 test_blink_led.py -v
``` 

## Electrical Connections

DUT | DOUBLE
------------ | -------------
2 | 21

Look at it! Here the DUT's output for led was intentionally PIN 2. This pin is connected to an embed led on devs Kit v1, and probably on other boards too. This allows us to see the led really blinking while the test is being performed. Only for visual purposes. 

![blinking](https://github.com/saramonteiro/micropython_test_lib/blob/master/images/blink.gif)
