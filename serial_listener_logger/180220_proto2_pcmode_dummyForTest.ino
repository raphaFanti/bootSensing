

//----------INCLUDING LIBRARIES---------------------------------------------------------------
#include <SPI.h> //lib for serial peripheral interface
#include <SD.h> //lib for sd card
#include <Q2HX711.h> //lib for HX711
#include <Wire.h> //needed for RTC
#include "RTClib.h" //lib for RTC
//#include <dht11.h> //lib for temperature & humidity

// Variables for red led blinking
int redledState = LOW;             // ledState used to set the LED
unsigned long previousblinkMillis = 0;        // will store last time LED was updated
const long interval = 500;

long id = 1; //store the id # of our reading

//----------SETUP LOOP------------------------------------------------------------------------------
void setup() {

  //Serial not needed in battery modus
    Serial.begin(9600); // start serial
    delay(3000); // wait for console opening

  //Serial not needed in battery modus
    while (!Serial) {
        ; // wait for serial port connection
    }
    Serial.print("Serial ready...");

   String header = "ID, strain1, strain2, strain3, strain4, strain5, strain6, temp [°C], runtime [ms]"; // file header
   Serial.println(header);

}

//-----------------------------------LOOP-------------------------------------------------------------------------
void loop() {

  float strain1out = 101.0;
  float strain2out = 102.0;
  float strain3out = 103.0;
  float strain4out = 104.0;
  float strain5out = 105.0;
  float strain6out = 106.0;

  int temp = 21;
  t0 = millis();

  //String filename_inuse = filename_new;
  String dataoutput = String(id) + ", " + String(strain1out) + ", " + String(strain2out) + ", " + String(strain3out) + ", " + String(strain4out) + ", " + String(strain5out) + ", " + String(strain6out) + ", " + String(temp) + ", " + String(t0);


  delay(100);

  id = id + 1;
}
