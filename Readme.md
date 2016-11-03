#AVRop VM PoC

PoC code for a ROP based movfuscator virtual machine running on a Harvard device.
ropMenu is a vulerable application for an Arduino Mega2560 where you can add and read notes over UART.
Find out more from [https://labs.mwrinfosecurity.com/blog/avrop](https://labs.mwrinfosecurity.com/blog/avrop)

##PoC
Compile ropMenu using Atmel Studio and dowload it to an Arduio Mega2560
You can connect to the application over UART on TX0/RX0:
screen /dev/ttyUSB0 38400 8N1

To exploit the appication run the ROP.py script with a payload
python ROP.py ../payloads/blink.bin
or
python ROP.py ../payloads/uart.bin
