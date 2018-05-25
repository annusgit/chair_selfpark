
short mot[] = {1, 2, 3, 4}; // motor 1 and 2
short t = 1000; 

void setup()
{
  for (int i=0; i<4; i++)
    pinMode(mot[i], OUTPUT); 
  // pinMode(mot2, OUTPUT); 
//  digitalWrite(pins[0], 1); // full speed 
//  digitalWrite(pins[5], 1);
}


void loop()
{
  digitalWrite(mot[2], 0); // full speed 
  digitalWrite(mot[3], 1);//does nothing 1001,0000
  //digitalWrite(pins[3], 0); // full speed 
  //digitalWrite(pins[4], 0);//left=0011   right=1100
  delay(t);
//  digitalWrite(pins[1], 0); // full speed 
  //digitalWrite(pins[2], 1);
  //digitalWrite(pins[3], 1); // full speed 
  //digitalWrite(pins[4], 1);
  //delay(t);
}
















