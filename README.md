# micropython_test_lib

Complete User Guide soon.

# Templates

# Running the Examples

# SPI Slave Module

# Troubleshooting

* If you're having problems to upload the files or if it's not injecting commands properly, the DUT or the double may have entered on raw repl mode. To check it, you may use the picocom or ohter terminal emulation tool. To work around this problem, and others, it's recommended to reset the boards.  This ensures there's no residual object. For problems like this, you should also check your cable and the configured USB port.  
* It's not recommended to interrupt tests since all tests have a routine of multiple steps from initialization to decommissioning. An interruption may lead to unexpected behavior. 
* This tool was designed to have all files pre-compiled before uploading, however, each firmware demands on a specific mpy-cross version. That's because many examples sent python files instead of micropython files. You may change the mpy-cross version in requirements.txt to pre-compile files for a specific firmware.
* SPI and BLE examples are unstable. The [5489 issue](https://github.com/micropython/micropython/issues/5489) reports an inconsistent init time for BLE module, that is very recent. This may cause problems during the text executions because the test relies on a deterministic time.   
* To track the commands that are sent and the results that are gathered through serial you may uncomment the line ```print (response)``` on the module ```serial_interface_upython.py```. This will help for debugging purposes.

# Future Works

It's intended to become this tool into a command line tool where dynamic parameters, such as USB port and others may be set on the terminal instead of being directly changed on code.  
