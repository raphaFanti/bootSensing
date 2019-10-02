
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

int numSens = sizeof(dataPins) / sizeof(dataPins[0]);

void setup() {
  Serial.begin(9600);
  

}

void loop() {
  Serial.print(numSens);
  

}
