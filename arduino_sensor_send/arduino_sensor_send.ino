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

// to delete afterwards
#define data_1 7 
#define clk_1 6
#define data_2 9
#define clk_2 8
#define data_3 11
#define clk_3 10
#define data_4  5
#define clk_4  4
#define data_5  3
#define clk_5  2
#define data_6 23
#define clk_6 22
#define data_7 25
#define clk_7 24
#define data_8 27
#define clk_8 26
#define data_9 29
#define clk_9 28
#define data_10 31
#define clk_10  30

// record button declarations
#define buttonPin 12
<<<<<<< HEAD
#define recordingLedPin 9

#define debug_flag false // NOT IN USE serves while code is running on serial monitor

// Strain gauges declaration (traditional style - to be improved)
Q2HX711 strain_1(data_1, clk_1); // Load Cell channel
Q2HX711 strain_2(data_2, clk_2);
Q2HX711 strain_3(data_3, clk_3);
Q2HX711 strain_4(data_4, clk_4);
Q2HX711 strain_5(data_5, clk_5);
=======
#define recordingLedPin 13

// Strain gauges declaration (hardcoded style - to be improved)
  Q2HX711 strain_1(data_1, clk_1); // Chan 1A
  Q2HX711 strain_2(data_2, clk_2); // Chan 1B
  Q2HX711 strain_3(data_3, clk_3); // Chan 2A
  Q2HX711 strain_4(data_4, clk_4); // Load Cell Y axis
  Q2HX711 strain_5(data_5, clk_5); // Load Cell X axis
  Q2HX711 strain_6(data_6, clk_6); // Chan 2B
  Q2HX711 strain_7(data_7, clk_7); // Chan 3A
  Q2HX711 strain_8(data_8, clk_8); // Chan 3B
  Q2HX711 strain_9(data_9, clk_9); // Chan 4A
  Q2HX711 strain_10(data_10, clk_10); // Chan 4B
>>>>>>> 0823b0f30fd802b005a26bffadb1cf5b027b3a6b

void setup() {
  
  Serial.begin(9600);
  
  // button pin mode declaration
  pinMode(buttonPin, INPUT);
  pinMode(recordingLedPin, OUTPUT);

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
  
<<<<<<< HEAD
  
=======
  //Serial.println("reading sensors...");

>>>>>>> 0823b0f30fd802b005a26bffadb1cf5b027b3a6b
  float reading_1 = strain_1.read();
  Serial.print(reading_1);

  float reading_2 = strain_2.read();
  Serial.print(",");
  Serial.print(reading_2);

  float reading_3 = strain_3.read();
  Serial.print(",");
  Serial.print(reading_3);
  
  float reading_4 = strain_4.read();
  Serial.print(",");
  Serial.print(reading_4);
  
  float reading_5 = strain_5.read();
<<<<<<< HEAD

  char msg[200];
  msg = msg + (int) reading_1;
  msg = msg + ",";
  Serial.println(msg);
  /* msg = msg + (int) reading_1;
  msg = msg + ",";
  msg = msg + (int) reading_3;
  msg = msg + ",";
  msg = msg + (int) reading_4;
  //msg = msg + ",";
  //msg = msg + (int) reading_5;
  */
  
  Serial.println(msg);

  
  // print in format reading_1,reading_2,...,reading_5 in utf-8
  /*
  Serial.print(reading_1);
  Serial.print(",");
  Serial.print(reading_2);
  Serial.print(",");
  Serial.print(reading_3);
  Serial.print(",");
  Serial.print(reading_4);
  Serial.print(",");
  Serial.println(reading_5);
  */
  
=======
  Serial.print(",");
  Serial.print(reading_5);

  float reading_6 = strain_6.read();
  Serial.print(",");
  Serial.print(reading_6);
  
  float reading_7 = strain_7.read();
  Serial.print(",");
  Serial.print(reading_7);
  
  float reading_8 = strain_8.read();
  Serial.print(",");
  Serial.print(reading_8);
>>>>>>> 0823b0f30fd802b005a26bffadb1cf5b027b3a6b
  
  float reading_9 = strain_9.read();
  Serial.print(",");
  Serial.print(reading_9);
  
  float reading_10 = strain_10.read();
  Serial.print(",");
  Serial.println(reading_10);
 
  delay(readingDelay); // pause between readings
  
}
