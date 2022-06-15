// this constant won't change:
const int  buttonPin = 2;    // the pin that the pushbutton is attached to
const int  buttonPin2 = 3;    // the pin that the pushbutton is attached to
const int ledPin = 13;       // the pin that the LED is attached to

// Variables will change:
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int buttonState2 = 0;  
int lastButtonState = 0;     // previous state of the button
int lastButtonState2 = 0;   

void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED as an output:
  pinMode(buttonPin2, INPUT);

  pinMode(ledPin, OUTPUT);
  // initialize serial communication:
  Serial.begin(19200);
  buttonState = LOW;
  buttonState2 = LOW;
}


void loop() {
  

  float analogButton0 = analogRead(A0);
  float analogButton1 = analogRead(A1);

  Serial.print(0);
  Serial.print(",");
  Serial.println(analogButton0);
  delay(50);

}
