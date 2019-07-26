
/*
 Oberalp - R&I Lab

 Acquisition of Strain Gauge data via HX711
 
 By: Raphael Fanti and Marilena Kurz
 Date: May 30th, 2019
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
 Version: 1.0

 This sketch uses the library described in https://makersportal.com/blog/2019/5/12/arduino-weighing-scale-with-load-cell-and-hx711

 Arduino Python specific code taken from: http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/

*/

#include <Q2HX711.h>

// runtime variables
const int readingDelay = 50;

// pin declarations
#define data_1  3
#define clk_1  2

#define data_2  6
#define clk_2  5

#define buttonPin 12

#define recordingLedPin 9

#define debug false // serves while code is running on serial monitor

// Strain gauges declaration
Q2HX711 strain_1(data_1, clk_1);
Q2HX711 strain_2(data_2, clk_2);

void setup() {
  Serial.begin(9600);
  
  // button pin mode declaration
  pinMode(buttonPin, INPUT);

}

int oldButtonState = LOW; // used to store and compare button states
int buttonState = LOW;
char receivedChar;

void loop() {

  // read button and detect edge
  buttonState = digitalRead(buttonPin);
  if(buttonState != oldButtonState && buttonState == HIGH)
    Serial.println("button_pressed");
  oldButtonState = buttonState;

  // receive status led indicator and act
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    if (receivedChar == 'b') // b is for begining of recording
      digitalWrite(recordingLedPin, HIGH);
    if (receivedChar == 'e') // e is for end of recording
      digitalWrite(recordingLedPin, LOW);
  }  

  // read sensor values
  float reading_1 = strain_1.read();
  float reading_2 = strain_2.read();
  
  if(debug){
    Serial.print("reading 1: ");
    Serial.print(reading_1);
    
    Serial.print(" , reading 2: ");
    Serial.println(reading_2);
  }
  else { // for graphing code: message is in format reading_1,reading_2 in utf-8
    Serial.print(reading_1);
    Serial.print(",");
    Serial.println(reading_2);
  }
  
  delay(readingDelay); // pause between readings
  
}
