
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
// declare each sensor, consisting of a pair (data, clock) to be included on each array
int dataPins[] = {3, 6};
int clockPins[] = {2, 5};

const int numSens = sizeof(dataPins) / sizeof(dataPins[0]);


// to delete afterwards
#define data_1  6
#define clk_1  5
#define data_2  1
#define clk_2  0
#define data_3  3
#define clk_3  2
#define data_4  8
#define clk_4  7
#define data_5  4
#define clk_5  10

// record button declarations
#define buttonPin 12
#define recordingLedPin 9

// Strain gauges declaration (traditional style - to be improved)
  Q2HX711 strain_1(data_1, clk_1); // Load Cell channel
  Q2HX711 strain_2(data_2, clk_2);
  Q2HX711 strain_3(data_3, clk_3);
  Q2HX711 strain_4(data_4, clk_4);
  //Q2HX711 strain_5(data_5, clk_5);

void setup() {
  
  Serial.begin(9600);

  //[to be implemented] Strain gauges declaration via array
  /*
  int stGauges[numSens];
  for (int i = 0; i < numSens; i++){
    Q2HX711 stGauge(dataPins[i], clockPins[i]);
    stGauges[i] = stGauge;
  }
  */
  
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
  
  //Serial.println("reading sensors...");

  float reading_1 = strain_1.read();
  Serial.print(reading_1);

  float reading_2 = strain_2.read();
  Serial.print(",");
  Serial.print(reading_2);

  //Serial.println("sensors read...");

  float reading_3 = strain_3.read();
  Serial.print(",");
  Serial.println(reading_3);
  
  //float reading_4 = strain_4.read();
  //float reading_5 = strain_5.read();

  
  
  /*
  Serial.print(reading_2);
  Serial.print(",");
  Serial.print(reading_3);
  Serial.print(",");  
  Serial.print(reading_4);
  Serial.print(",");
  Serial.println(reading_5);
  */
  
  delay(readingDelay); // pause between readings
  
}
