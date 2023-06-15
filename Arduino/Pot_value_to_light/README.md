This code was used for initial testing of the line light and to figure out how exactly to control it through TCP/IP.

A potentiometer was read by the arduino, and using this information, a light command was constructed that could be send to the power source of the line light.
To make this happen, an ethernet shield was placed on the arduino, and the shield and the power source were connected with an ethernet cable.

libraries needed: SPI and Ethernet (both are included in the standard library)

Settings on power source:
- Set control to "Ethernet TCP"
- Read the ip adress and port and fill them into the program.