
#include <SoftwareSerial.h>
SoftwareSerial mySerial(9, 8); // RX, TX
String command; 
int indicator_led = 13, t = 50;

void setup() {
  // Open serial communications:
  Serial.begin(9600);
  while (!Serial) { // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println("Let's see if this works!");
 
  // The HC-06 defaults to 9600 according to the datasheet.
  mySerial.begin(9600);
  pinMode(indicator_led, OUTPUT);
}


void loop()
{  
  // Read device output if available.
  if (mySerial.available()) 
  {
    digitalWrite(indicator_led, 1);
    while(mySerial.available()) 
    { // While there is more to be read, keep reading.
      command += (char)mySerial.read();
    }
    Serial.println(command);   
    digitalWrite(indicator_led, 0);
    
    mySerial.println(command);   
 }
  command = ""; // No repeats, so reset!
  delay(t);
}




