#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x89, 0xD8 }; // MAC address of the Ethernet shield
IPAddress ip(192, 168, 0, 50); // IP address of the Arduino board
IPAddress server(192, 168, 0, 2); // IP address of the device you're controlling
int port = 40001; // Port number to use for the TCP connection

EthernetClient client;

float PPR = 16;
float diameter = 0.063;  // diameter of encoder disc in m
float pulseCount = 0;
long currentTime = 0;
long prevTime = 0;
long deltaT = 0;  // time between pulses in ms
float speed = 0;
int speedUpdate = 1000;

float maxSpeed = 1;
int brightness = 0;

String potValString = "";
String lightCommand = "";
String lightCommandInit = "@00MD1100\r\n";
int setRange = 0;

void setup() {
  Ethernet.begin(mac, ip);
  Serial.begin(9600); // Initialize serial communication
  delay(1000); // Wait for Ethernet to initialize

  pinMode(2, INPUT_PULLUP); // Set pin 2 as input with pull-up resistor enabled
  attachInterrupt(digitalPinToInterrupt(2), interruptHandler, FALLING); // Attach interrupt handler to pin 2, trigger on falling edge
}

void loop() {

  if (client.connect(server, port)) {
      // Serial.println("Connected to server");
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
        // Serial.print(c);
      }
      client.stop();
      // Serial.println("\nDisconnected from server");
    } else {
      // Serial.println("Failed to connect to server");
    }
  
  currentTime = millis();
    if ((currentTime - prevTime) > speedUpdate){
      prevTime = millis();
      speed = (pulseCount/PPR)*PI*diameter;
      brightness = (speed/maxSpeed)*1023;
      if (brightness > 1023){
        brightness = 1023;
      }

      potValString = brightness;
      while (potValString.length() < 4)  {
        potValString = "0" + potValString;
      }
      lightCommand = "@00F" + potValString + "\r\n";

      Serial.println(speed);
      pulseCount = 0;
    }
  
}

void interruptHandler() {
  pulseCount++;
  }

