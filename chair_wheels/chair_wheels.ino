
short pins[] = {0, 1, 2, 3, 4, 5}; // 0 and 5 are enable pins and in the middle we have the controls
short t = 1000; 

void setup()
{
  for (int i=0; i<6; i++)
     pinMode(pins[i], OUTPUT); 
  analogWrite(pins[0], 255); // full speed 
  analogWrite(pins[5], 255);
}


void loop()
{
  digitalWrite(pins[1], 1); // full speed 
  digitalWrite(pins[2], 0);
  digitalWrite(pins[3], 1); // full speed 
  digitalWrite(pins[4], 0);
  delay(t);
  digitalWrite(pins[1], 0); // full speed 
  digitalWrite(pins[2], 1);
  digitalWrite(pins[3], 0); // full speed 
  digitalWrite(pins[4], 1);
  delay(t);
}
