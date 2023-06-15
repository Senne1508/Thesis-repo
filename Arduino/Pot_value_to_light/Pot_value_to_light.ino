#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x89, 0xD8 }; // MAC address of the Ethernet shield
IPAddress ip(192, 168, 0, 50); // IP address of the Arduino board
IPAddress server(192, 168, 0, 2); // IP address of the device you're controlling
int port = 40001; // Port number to use for the TCP connection

EthernetClient client;

String potValString = "";
String lightCommand = "";
String lightCommandInit = "@00MD1100\r\n";
int setRange = 0;

void setup() {
  Ethernet.begin(mac, ip);
  Serial.begin(9600);
  delay(1000); // Wait for Ethernet to initialize
}

void loop() {

  int potVal = analogRead(A0);    // Potentiometer was connected to the A0 analog input of the arduino.
  potValString = potVal;

  // Uing the value of the potatiometer (between 0-1023), a clight command was constructed. The light command consists of a string of charactersthat can be send over TCP/IP.
  // A full list of commands for the power supply can be found in the documentation of the power supply.
  while (potValString.length() < 4)  {
    potValString = "0" + potValString;
  }
  lightCommand = "@00F" + potValString + "\r\n";

  // The following code sends the constructed command to the power source over TCP/IP and listens for messages from the power source.
  if (client.connect(server, port)) {
    Serial.println("Connected to server");
    if (setRange == 0){
      setRange = 1;
      client.print(lightCommandInit);      
    }
    else{
      client.print(lightCommand);
    }
    delay(10); // Wait for the device to respond
    while (client.available()) {
      char c = client.read();
      Serial.print(c);
    }
    client.stop();
    Serial.println("\nDisconnected from server");
  } else {
    Serial.println("Failed to connect to server");
  }
  //delay(10); // Wait before trying again
}