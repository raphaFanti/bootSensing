
/*
 Oberalp - R&I Lab

 Acquisition of Strain Gauge data via HX711
 
 By: Raphael Fanti and Marilena Kurz
 Date: May 30th, 2019
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
 Version: 1.0

 This example code uses bogde's excellent library: https://github.com/bogde/HX711
 bogde's library is released under a GNU GENERAL PUBLIC LICENSE

 Arduino Python specific code taken from:
 http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/

 The HX711 board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.

*/

#include "HX711.h"

#define data_1  3
#define clk_1  2

#define data_2  6
#define clk_2  5

#define calib_measures 20

#define debug true // serves while code is running on serial monitor

// Strain gauges declaration
// [ToDo] to be done via array in the future for several units
HX711 strain_1;
float offset_1 = 0; 
float calib_1 = -7050; // to be refined via calibration

HX711 strain_2;
float offset_2 = 0; 
float calib_2 = -7050; // to be refined via calibration

void setup() {
  Serial.begin(9600);

  // Initiation and tare of gauges
  // [ToDo] to be done via array in the future for several units
  strain_1.begin(data_1, clk_1);
  strain_1.set_scale(calib_1);
  //strain_1.tare(); //Reset the scale to 0, below method is preffered
  long zero_factor_1 = strain_1.read_average(calib_measures); //Get a baseline of readings
  strain_1.set_offset(zero_factor_1);
  
  strain_2.begin(data_2, clk_2);
  strain_2.set_scale(calib_2);
  //strain_2.tare(); //Reset the scale to 0, below method is preffered
  long zero_factor_2 = strain_2.read_average(calib_measures); //Get a baseline of readings
  strain_2.set_offset(zero_factor_2);

}

void loop() {

  float reading_1 = strain_1.get_units();
  float reading_2 = strain_2.get_units();
  
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
  
  delay(250); // pause between readings
  
}
