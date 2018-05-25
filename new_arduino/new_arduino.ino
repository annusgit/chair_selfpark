
#include <SoftwareSerial.h>
SoftwareSerial mySerial(9, 8); // RX, TX

String command = ""; // Stores response of the HC-06 Bluetooth device
String state = "idle";
short indicator_led = 13; 
short pins[] = {1, 2, 3, 4}; // 0 and 5 are enable pins and in the middle we have the controls
short en1 = 0, en2 = 5;
short t = 2000;

void setup() {
  // Open serial communications:
  Serial.begin(9600);
  while (!Serial) { // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println("Type AT commands!");
  
  // The HC-06 defaults to 9600 according to the datasheet.
  mySerial.begin(9600);
  
  pinMode(indicator_led, OUTPUT);
  //pinMode(en1, OUTPUT); 
  //pinMode(en2, OUTPUT); 
  // motor initilizations
  for (int i=0; i<4; i++)
     pinMode(pins[i], OUTPUT); 
  //analogWrite(en1, 120);
  //analogWrite(en2, 120);
}

void loop() {
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
    
    if (received == 1)
    {
        /*if (state != "up")
           {
             state = "up";
             idle();
           }*/
        Serial.println(state);
        idle();
    }

    else if (received == 2)
    {
        /*if (state != "up")
           {
             state = "up";
             idle();
           }*/
        Serial.println(state);
        idle();
    }

    else if (received == 3)
    {
        /*if (state != "up")
           {
             state = "up";
             idle();
           }*/
        Serial.println(state);
        idle();
    }

    else if (received == 4)
    {
        /*if (state != "up")
           {
             state = "up";
             idle();
           }*/
        Serial.println(state);
        idle();
    }
    
    else if (received == 0)
    {
        /*if (state != "up")
           {
             state = "up";
             idle();
           }*/
        Serial.println(state);
        idle();
    }
   
    command = ""; // No repeats
    digitalWrite(indicator_led, 0);
  }
  delay(t);
  
  // Read user input if available.
  if (Serial.available()){
    delay(t); // The delay is necessary to get this working!
    mySerial.write(Serial.read());
  }
  
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
  digitalWrite(pins[0], 1);  // mot1-01, mot2-10
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 1);
  digitalWrite(pins[3], 0); 
}


// we won't need this
void down()
{
  digitalWrite(pins[0], 0); // full speed 
  digitalWrite(pins[1], 1);
  digitalWrite(pins[2], 0); // full speed 
  digitalWrite(pins[3], 1); 
}


void right()
{
  digitalWrite(pins[0], 1); // full speed 
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 0); // full speed 
  digitalWrite(pins[3], 0); 
}


void left()
{
  digitalWrite(pins[0], 0); // full speed 
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 1); // full speed 
  digitalWrite(pins[3], 0); 
}


void idle()
{
  digitalWrite(pins[0], 0); // full speed 
  digitalWrite(pins[1], 0);
  digitalWrite(pins[2], 0); // full speed 
  digitalWrite(pins[3], 0); 
}






