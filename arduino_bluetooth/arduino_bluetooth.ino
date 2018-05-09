

// some function signatures
void rename();

// global vars
String message;
short indicator_led = 13;

void setup() 
{
  Serial.begin(9600);
  Serial.println("serial-delimit-21"); // so I can keep track of what is loaded
  
  pinMode(indicator_led, OUTPUT);
}


void loop() {

  //expect a string like wer,qwe rty,123 456,hyre kjhg,
  //or like hello world,who are you?,bye!,
  while (Serial.available()) {
    digitalWrite(indicator_led, 1);
    delay(10);  //small delay to allow input buffer to fill

    char c = Serial.read();  //gets one byte from serial buffer
    if (c == ',') {
      break;
    }  //breaks out of capture loop to print readstring
    message += c; 
    
    digitalWrite(indicator_led, 0);
  } //makes the string readString  

  if (message.length() >0) {
    Serial.println(message); //prints string to serial port out

    message = ""; //clears variable for new input
  }
}


//////////////////////////////////////////////////////////////////////////////////
// utility funcs

// this function in case you want to rename your hc-06 device
void rename()
{
  Serial.begin(9600); 
  delay(5000);
  Serial.print("AT+chair");
  delay(2000);
}

