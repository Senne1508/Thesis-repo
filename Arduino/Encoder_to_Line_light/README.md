This code controls the line light based on the conveyor belt speed.

The Arduino reads the encoder signals and uses these to calculate the speed.
This speed information is converted to the necessary illumination.
A command is constructed that can be sent over TCP-IP using an arduino ethernet shield.
