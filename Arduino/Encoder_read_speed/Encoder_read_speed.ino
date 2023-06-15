float PPR = 16;           // pulses per rotation of encoder
float diameter = 0.0632;  // diameter of roller in m
float pulseCount = 0;
long currentTime = 0;
long prevTime = 0;
float speed = 0;
int speedUpdate = 1000;   // time between speed updates in [ms] longer time --> more accurate speed.


void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(2, INPUT_PULLUP); // Set pin 2 as input with pull-up resistor enabled
  attachInterrupt(digitalPinToInterrupt(2), interruptHandler, FALLING); // Attach interrupt handler to pin 2, trigger on falling edge
}

void loop() {
  currentTime = millis();
  if ((currentTime - prevTime) > speedUpdate){
    prevTime = millis();
    speed = (pulseCount/PPR)*PI*diameter;
    Serial.println(speed);
    pulseCount = 0;
  }
  
}

void interruptHandler() {
  pulseCount++;
  }

