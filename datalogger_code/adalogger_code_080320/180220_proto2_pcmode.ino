/*
 Oberalp - R&I Lab
 Acquisition of Strain Gauge data via HX711
 
 By: Raphael Fanti and Marilena Kurz
 Date: May 30th, 2019 (first try)
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
 Version: 1.0
 This sketch uses the library described in https://makersportal.com/blog/2019/5/12/arduino-weighing-scale-with-load-cell-and-hx711
 Arduino Python specific code taken from: http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/
 SD card datalogger -> code is in the public domain. (by Tom Igoe)
 State change detection (edge detection) -> code is in the public domain. (by Tom Igoe)
 Timestamp function using a DS1307 RTC

--------------------USER GUIDE-----------------------------------------------------------------
- to create a new file switch on/off
- press the green button to start/end acquiring the baseline
- press the red button to start/end recording of experiment
- green led on -> ready/SD detected
- red light blinking -> baseline acquiring
- red light on -> recording data
*/

//----------INCLUDING LIBRARIES---------------------------------------------------------------
#include <SPI.h> //lib for serial peripheral interface
#include <SD.h> //lib for sd card
#include <Q2HX711.h> //lib for HX711
#include <Wire.h> //needed for RTC
#include "RTClib.h" //lib for RTC
//#include <dht11.h> //lib for temperature & humidity

//----------DEFINING PINS, VARIABLES & FUNCTIONS-----------------------------------------------
const int chipSelect = 4; //port for sd card

//Variables for hx711 -> 1 LOADCELL AND 1 STRAIN GAUGE IN USE
const int DOUT1 = 6; //strain gauge 1 data
const int CLK1 = 5; //strain gauge 1 clock

const int DOUT2 = 10; //strain gauge 2 data
const int CLK2 = 9; //strain gauge 2 clock

const int DOUT3 = 12; //strain gauge 3 data 
const int CLK3 = 11; //strain gauge 3 clock

//const int DOUT4 = A0; //strain gauge 4 data
//const int CLK4 = 13; //strain gauge 4 clock -> to define Pin as input

//Variables for LEDS and Button
const int redledPin = A3; //red led pin (data acquisition on going)
const int greenledPin = A4;//green led pin (no data acquisition,system ready)
const int buttonPin_rec = A2; //button pin for recording
const int buttonPin_base = A1; //button pin for baseline

int buttonPushCounter_rec = 0; // counter for the number of recording button presses
int buttonState_rec = 0; //current recording button state
int lastButtonState_rec = 0; // previous state of the recording button
int buttonPushCounter_base = 0; // counter for the number of baseline button presses
int buttonState_base = 0; //current baseline button state
int lastButtonState_base = 0; // previous state of the baseline button

// Variables for red led blinking
int redledState = LOW;             // ledState used to set the LED
unsigned long previousblinkMillis = 0;        // will store last time LED was updated
const long interval = 500; 

long id = 1; //store the id # of our reading

//unsigned long offsettime; //offset from start rectime
unsigned long t0;
unsigned long t;
unsigned long currentmillis;
String filename; // create filename variable for baseline

//#define DHT11_PIN 13 //data pin temperature&humidity

//Functions for hx711
Q2HX711 strain1(DOUT1,CLK1); //strain gauge 1
Q2HX711 strain2(DOUT2,CLK2); //strain gauge 2
Q2HX711 strain3(DOUT3,CLK3); //strain gauge 3
//Q2HX711 strain4(DOUT4,CLK4); //strain gauge 4

//Function for RTC with date, time & temperature
RTC_DS3231 rtc;

//Function for DHT11 (temp&hum)
//dht11 DHT;


//----------SETUP LOOP------------------------------------------------------------------------------
void setup() {

  //Serial not needed in battery modus
    Serial.begin(9600); // start serial
    delay(3000); // wait for console opening

  //Temperature sensor not in use at the moment
    //int chk = DHT.read(DHT11_PIN);
    //int temp = DHT.temperature;
    //int humidity = DHT.humidity;
  
  //Serial not needed in battery modus
    while (!Serial) {
        ; // wait for serial port connection
    }
    Serial.print("Initializing SD card..."); //initializing sd card
  
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed"); // sd card not found
       while (1);
   }
  Serial.println("card initialized."); //sd card ok
  
  if (! rtc.begin()) { //check if RTC available
      Serial.println("Couldn't find RTC"); //errore message if not found
     while (1);
   }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, lets set the time!"); //error message if no power
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); //set time via PC
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
    
  }

  pinMode(redledPin, OUTPUT); // define redledPin as output for data acquisition
  pinMode(greenledPin,OUTPUT); //define greenledPin as output for system ready
  pinMode(buttonPin_rec, INPUT); // define buttonPin as input
  pinMode(buttonPin_base, INPUT); // define buttonPin base as input
  //pinMode(DOUT4, INPUT); // define CLK4 as input


  //RTC Function & variables
  DateTime now = rtc.now(); //date & time

  int year_2digit = (now.year()-2000); //get year as 2 digit
  int temp = rtc.getTemperature(); //get temperature from RTC

//Construct filename (maxiumum digit # of filename = 12)
  filename = String(year_2digit) + String(now.month()) + String(now.day()) + String(now.minute()) + String(".txt");
  //filename_rec =  String("r") + String(year_2digit) + String(now.month()) + String(now.day()) + String(now.minute()) + String(".txt");

  File dataFile = SD.open(filename,FILE_WRITE); //open file 

   String actual_date = String(now.day()) + "." + String(now.month()) + "." + String(now.year()); //actual date
   String actual_time = String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second()); //actual time
   String userinfo = "Date: " + actual_date + " , In use by: Mena"; //user info
   String infoline_start = "Daytime: " + actual_time + ", Temperature: " + String(temp) + "°C";// file infoline
   String header = "ID, strain1, strain2, strain3, temp [°C], runtime [ms]"; // file header
 
  if (dataFile){ //if file is available write sensor data
    //dataFile.println(",,"); //blank line in case there where previous data
    File dataFile = SD.open(filename, FILE_WRITE); //open baseline file
    dataFile.println(userinfo); //print user info in datafile
    dataFile.println(infoline_start); //printing general info in datafile
    dataFile.println(header); //writing header in datafile
    dataFile.close();
    Serial.println(userinfo); //print user info on Serial
    Serial.println(infoline_start); //print infoline on Serial
    Serial.println(header); // print also sensor data to Serial
  }
  
  else {
    Serial.println("error creating datafile"); // error message if file not open
  } 

}

//-----------------------------------------blinkblink------------------------------------------------------------
//Function red led blinking
void blinkblink() {
  unsigned long currentblinkMillis = millis();

  if (currentblinkMillis - previousblinkMillis >= interval) {
    // save the last time you blinked the LED
    previousblinkMillis = currentblinkMillis;

    // if the LED is off turn it on and vice-versa:
    if (redledState == LOW) {
      redledState = HIGH;
    } else {
      redledState = LOW;
    }

    // set the LED with the ledState of the variable:
    digitalWrite(redledPin, redledState);
  }
}

//-----------------------------------LOOP-------------------------------------------------------------------------
void loop() {
 
  float strain1out = strain1.read(); // reading HX711 from strain gauge 1
  float strain2out = strain2.read(); // reading HX711 from strain gauge 2
  float strain3out = strain3.read(); // reading HX711 from strain gauge 3
  //float strain4out = strain4.read(); // reading HX711 from strain gauge 4
  //int chk = DHT.read(DHT11_PIN);
  //int temp = DHT.temperature;
  //int humidity = DHT.humidity;
  DateTime now = rtc.now(); //date & time
  int temp = rtc.getTemperature();
  t0 = millis();
  
  String actual_time = String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second()); //actual time
  //String filename_inuse = filename_new;
  String dataoutput = String(id) + ", " + String(strain1out) + ", " + String(strain2out) + ", " + String(strain3out) + ", " + String(temp) + ", " + String(t);

  buttonState_rec = digitalRead(buttonPin_rec); //read state of recording button
  buttonState_base = digitalRead(buttonPin_base); //read state of baseline button
  

  if(buttonState_base != lastButtonState_base){
    
    if (buttonState_base == HIGH) {//if button pressed
      buttonPushCounter_base++; 
      id = 1; //reset index
      currentmillis = t0;
      File dataFile = SD.open(filename,FILE_WRITE); //open dataFile 
      dataFile.println("BASELINE Time: " + actual_time);
      dataFile.close();
      Serial.println("BASELINE Time: " + actual_time);
    }
     lastButtonState_base = buttonState_base;
     t = 0;
     
  } 

  if ((buttonPushCounter_base % 2 == 1) && (buttonPushCounter_rec % 2 == 0 || buttonPushCounter_rec % 2 == 1)) {
    digitalWrite(greenledPin, LOW);
    blinkblink(); //function red led blinking
    t = t0 - currentmillis; //reset millis
    File dataFile = SD.open(filename,FILE_WRITE); //open dataFile 
    dataFile.println(dataoutput); //print sensor data to datafile
    dataFile.close();
    Serial.println(dataoutput); // print also sensor data to serial
    id++; //Increment ID number for row
    }
    else {
   digitalWrite(redledPin, LOW);
   digitalWrite(greenledPin, HIGH);
  }
 
  
  if(buttonState_rec != lastButtonState_rec) {//compare current and last button states
   //if state has changed (button pressed)
   
    if (buttonState_rec == HIGH) {//if button pressed
      buttonPushCounter_rec++; 
      id = 1; //reset index
      currentmillis = t0;
      File dataFile = SD.open(filename,FILE_WRITE); //open dataFile 
      dataFile.println("RECORDING Time: " + actual_time);
      dataFile.close();
     Serial.println("RECORDING Time: " + actual_time);
    }
      lastButtonState_rec = buttonState_rec;
     t = 0;
      
  }

  if ((buttonPushCounter_rec % 2 == 1) && (buttonPushCounter_base % 2 == 0 || buttonPushCounter_base % 2 == 1)) {
    digitalWrite(greenledPin, LOW);
    digitalWrite(redledPin, HIGH);
    t = t0 - currentmillis; //reset millis
    File dataFile = SD.open(filename,FILE_WRITE); 
    dataFile.println(dataoutput); //print sensor data to datafile
    dataFile.close();
    Serial.println(dataoutput); // print also sensor data to serial
    id++; //Increment ID number for row
  } else {
    if(buttonPushCounter_base % 2 == 0){
    digitalWrite(redledPin, LOW);
    digitalWrite(greenledPin, HIGH);
    }
}  
  
  //delay(1000);
}
