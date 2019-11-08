#include <Q2HX711.h>


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
#define data_1  6
#define clk_1  5

// Strain gauges declaration (traditional style - to be improved)
Q2HX711 strain_1(data_1, clk_1); // Load Cell channel

int oldTime = millis();
int newTime;

void setup() {
  
  Serial.begin(9600);

}

void loop() {

  // read sensor values
  float reading_1 = strain_1.read();
  newTime = millis();
  float freq = 1.0 / (newTime - oldTime);
  Serial.print(freq);

  oldTime = newTime;
  delay(readingDelay); // pause between readings
  
}
