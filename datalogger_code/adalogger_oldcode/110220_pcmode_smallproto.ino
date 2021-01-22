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
const int DOUT0 = 5; //strain gauge 1
const int CLK0 = 6; //strain gauge 1

const int DOUT1 = 9; //strain gauge 2
const int CLK1 = 10; //strain gauge 2

//Variables for LEDS and Button
const int redledPin = A4; //red led pin (data acquisition on going)
const int greenledPin = A5;//green led pin (no data acquisition,system ready)
const int buttonPin_rec = A3; //button pin for recording
const int buttonPin_base = A2; //button pin for baseline

int buttonPushCounter_rec = 0; // counter for the number of recording button presses
int buttonState_rec = 0; //current recording button state
int lastButtonState_rec = 0; // previous state of the recording button
int buttonPushCounter_base = 0; // counter for the number of baseline button presses
int buttonState_base = 0; //current baseline button state
int lastButtonState_base = 0; // previous state of the baseline button

long id = 1; //store the id # of our reading
//int n = 0; //variable for increment file number

//unsigned long offsettime; //offset from start rectime
unsigned long t;
String filename; //create filename variable

//#define DHT11_PIN 13 //data pin temperature&humidity

//Functions for hx711
Q2HX711 strain1(DOUT0,CLK0); //loadcell
Q2HX711 strain2(DOUT1,CLK1); //strain gauge 1

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


  //RTC Function & variables
  DateTime now = rtc.now(); //date & time

  int year_2digit = (now.year()-2000); //get year as 2 digit
  int temp = rtc.getTemperature(); //get temperature from RTC

//Construct filename (maxiumum digit # of filename = 12)
  filename =  String(year_2digit) + String(now.month()) + String(now.day()) + String(now.minute()) + String(".txt");

  File dataFile = SD.open(filename,FILE_WRITE); //open file 
    //  if (SD.exists(filename)){
    //    filename[6]++;
    //    String filename =  String(year_2digit) + String(now.month()) + String(now.day()) + String(n) + String(".txt"); //update filename
    //    File dataFile = SD.open(filename,FILE_WRITE);
    //    //Serial.println("New File: " + filename + " created!"); //show new filename on Serial
    //    filename_new = filename;
    //  }
    //  else{
    //   //Serial.println("Filename:" + filename); //show filename
    //   filename_new = filename;
    //  }
    
   String actual_date = String(now.day()) + "." + String(now.month()) + "." + String(now.year()); //actual date
   String actual_time = String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second()); //actual time
   String userinfo = "Date: " + actual_date + " , In use by: Mena"; //user info
   String infoline_start = "Daytime: " + actual_time + ", Temperature: " + String(temp) + "°C";// file infoline
   String header = "ID, strain1, strain2, temperature [°C], runtime [ms]"; // file header
 
  if (dataFile) { //if file is available write sensor data
    //dataFile.println(",,"); //blank line in case there where previous data
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

//-----------------------------------LOOP-------------------------------------------------------------------------
void loop() {
 
  float strain1out = strain1.read(); // reading HX711 from loadcell
  float strain2out = strain2.read(); // reading HX711 from strain gauge 1
  //int chk = DHT.read(DHT11_PIN);
  //int temp = DHT.temperature;
  //int humidity = DHT.humidity;
  DateTime now = rtc.now(); //date & time
  int temp = rtc.getTemperature();
  t = millis();
  unsigned long previous_offsettime = 0;
  //unsigned long current_offsettime = millis(); 
  //offsettime = millis();
  String actual_time = String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second()); //actual time
  //String filename_inuse = filename_new;
  String dataoutput = String(id) + ", " + String(strain1out) + ", " + String(strain2out) + "," + String(temp) + "," + String(t);

  buttonState_rec = digitalRead(buttonPin_rec); //read state of recording button
  buttonState_base = digitalRead(buttonPin_base); //read state of baseline button
  
  File dataFile = SD.open(filename,FILE_WRITE); //open dataFile 

  if(buttonState_base != lastButtonState_base){
    if (buttonState_base == HIGH) {//if button pressed
      buttonPushCounter_base++; 
      id = 1; //reset index
      dataFile.println("BASELINE Time: " + actual_time);
      dataFile.close();
      Serial.println("BASELINE Time: " + actual_time);
    }
     lastButtonState_base = buttonState_base;
  } 

  if ((buttonPushCounter_base % 2 == 1) && (buttonPushCounter_rec % 2 == 0 || buttonPushCounter_rec % 2 == 1)) {
    digitalWrite(greenledPin, LOW);
    digitalWrite(redledPin, HIGH);
    delay(500);
    digitalWrite(redledPin, LOW);
    delay(500);
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
   //offsettime = current_offsettime - previous_offsettime;
    if (buttonState_rec == HIGH) {//if button pressed
      buttonPushCounter_rec++; 
      id = 1; //reset index
      dataFile.println("RECORDING Time: " + actual_time);
      dataFile.close();
     Serial.println("RECORDING Time: " + actual_time);
    }
      lastButtonState_rec = buttonState_rec;
    //previous_offsettime = current_offsettime;
  }

  if ((buttonPushCounter_rec % 2 == 1) && (buttonPushCounter_base % 2 == 0 || buttonPushCounter_base % 2 == 1)) {
    digitalWrite(greenledPin, LOW);
    digitalWrite(redledPin, HIGH);
   
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
