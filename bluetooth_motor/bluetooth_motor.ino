
#include <MPU6050_6Axis_MotionApps20.h>
#include <I2Cdev.h>
#include <Wire.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(9, 8); // RX, TX

String command = ""; // Stores response of the HC-06 Bluetooth device
String state = "idle";
short indicator_led = 13; 
short pins[] = {4, 5, 6, 7}; // 0 and 5 are enable pins and in the middle we have the controls
short t = 50;

void up();
void down();
void right();
void left();
void idle();
void Blue_motors();
void test_motors();
void command_to_int();


void setup() {
  // Open serial communications:
  Serial.begin(9600);
  while (!Serial) { // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println("Type AT commands!");
 
  // The HC-06 defaults to 9600 according to the datasheet.
  mySerial.begin(9600);
  
  pinMode(indicator_led, OUTPUT);
  // motor initilizations
  for (int i=0; i<4; i++)
     pinMode(pins[i], OUTPUT); 
}


void loop()
{
  Blue_motors();
}


void Blue_motors() 
{
  // Read device output if available.
  if (mySerial.available()) 
  {
    digitalWrite(indicator_led, 1);
    while(mySerial.available()) 
    { // While there is more to be read, keep reading.
      command += (char)mySerial.read();
    }
    // Serial.println(command);
   
    int received = command_to_int(command);
    Serial.print(received);
    
    switch(received)
    {
        case 1:
          Serial.println(state);
          up();
          break;
          
        case 2:
          Serial.println(state);
          down();
          break;
          
        case 3:
          Serial.println(state);
          left();
          break;
          
        case 4:
          Serial.println(state);
          right();
          break;
          
        case 0:
          Serial.println(state);
          idle();
          break;
          
        default:
          break;
    }
    
    command = ""; // No repeats
    digitalWrite(indicator_led, 0);
  }
  delay(t);
  
  // Read user input if available.
  //if (Serial.available()){
  //  delay(t); // The delay is necessary to get this working!
  //  mySerial.write(Serial.read());
  //}
  
  // 
  //delay(t);
}

short command_to_int(String command)
{
  if (command == "idle")
    return 0;
  else if (command == "up")
    return 1;
  else if (command == "down")
    return 2;
  else if (command == "left")
    return 3;  
  else if (command == "right")
    return 4;
}

void up()
{
  digitalWrite(pins[0], 0);  // mot1-01, mot2-10
  digitalWrite(pins[1], 1);
  digitalWrite(pins[2], 0);
  digitalWrite(pins[3], 1); 
}


void down()
{
  digitalWrite(pins[0], 1); // full speed 
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 1); // full speed 
  digitalWrite(pins[3], 0); 
}


void left()
{
  digitalWrite(pins[0], 0); // full speed 
  digitalWrite(pins[1], 1);
  digitalWrite(pins[2], 0); // full speed 
  digitalWrite(pins[3], 0); 
}


void right()
{
  digitalWrite(pins[0], 0); // full speed 
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 0); // full speed 
  digitalWrite(pins[3], 1); 
}


void idle()
{
  digitalWrite(pins[0], 0); // full speed 
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 0); // full speed 
  digitalWrite(pins[3], 0); 
}


void test_motors()
{
  up();	
  delay(t);
  down();
  delay(t);
  right();
  delay(t);
  left();
  delay(t);
}





