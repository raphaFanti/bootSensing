/*
 Oberalp - R&I Lab
 Acquisition of Strain Gauge data via HX711
 
 By: Raphael Fanti and Marilena Kurz
 Date: May 30th, 2019
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
 Version: 1.0
 This sketch uses the library described in https://makersportal.com/blog/2019/5/12/arduino-weighing-scale-with-load-cell-and-hx711
 Arduino Python specific code taken from: http://www.toptechboy.com/tutorial/python-with-arduino-lesson-11-plotting-and-graphing-live-data-from-arduino-with-matplotlib/
 SD card datalogger -> code is in the public domain. (by Tom Igoe)
 State change detection (edge detection) -> code is in the public domain. (by Tom Igoe)
Timestamp function using a DS1307 RTC
*/
//TO DO: check RTC time&date, controll filename (Setup&Loop->does it remain the same?, filecounter), implement a "new run function"?

//----------INCLUDING LIBRARIES---------------------------------------------------------------
#include <SPI.h> //lib for serial peripheral interface
#include <SD.h> //lib for sd card
#include <Q2HX711.h> //lib for HX711
#include <Wire.h> //needed for RTC
#include "RTClib.h" //lib for RTC
#include <dht11.h> //lib for temperature & humidity

//----------DEFINING PINS, VARIABLES & FUNCTIONS-----------------------------------------------
const int chipSelect = 4; //port for sd card

//Variables for hx711 -> 1 LOADCELL AND 1 STRAIN GAUGE IN USE
const int DOUT0 = 5; //loadcell data
const int CLK0 = 6; //loadcell clock

const int DOUT1 = 9; //strain gauge 1
const int CLK1 = 10; //strain gauge 1

//Variables for LEDS and Button
const int redledPin = A4; //red led pin (data acquisition on going)
const int greenledPin = A5;//green led pin (no data acquisition,system ready)
const int buttonPin = 12; //button pin

int buttonPushCounter = 0; // counter for the number of button presses
int buttonState = 0; //current button state
int lastButtonState = 0; // previous state of the button

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}; //definition of days

long id = 1; //store the id # of our reading
int n = 0; //variable for increment file number

unsigned long offsettime; //offset from start rectime

#define DHT11_PIN 13 //data pin temperature&humidity

//Functions for hx711
Q2HX711 loadcell(DOUT0,CLK0); //loadcell
Q2HX711 strain1(DOUT1,CLK1); //strain gauge 1

//Function for RTC (timestamp)
RTC_DS3231 rtc;

//Function for DHT11 (temp&hum)
dht11 DHT;

//----------SETUP LOOP------------------------------------------------------------------------------
void setup() {
  
  Serial.begin(9600); // start serial
  //delay(3000); // wait for console opening
  
  int chk = DHT.read(DHT11_PIN);
  //int temp = DHT.temperature;
  int humidity = DHT.humidity;
  
  
  while (!Serial) {
    ; // wait for serial port connection
  }
  
   if (! rtc.begin()) { //check if RTC available
    Serial.println("Couldn't find RTC"); //errore message if not found
    while (1);
  }
//
  if (rtc.lostPower()) {
    Serial.println("RTC lost power, lets set the time!"); //error message if no power
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); //set time via PC
//    // This line sets the RTC with an explicit date & time, for example to set
//    // January 21, 2014 at 3am you would call:
//    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }
  
  Serial.print("Initializing SD card..."); //initializing sd card
  
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed"); // sd card not found
    
    while (1);
  }
  Serial.println("card initialized."); //sd card ok

  pinMode(redledPin, OUTPUT); // define redledPin as output for data acquisition
  pinMode(greenledPin,OUTPUT); //define greenledPin as output for system ready
  pinMode(buttonPin, INPUT); // define buttonPin as input
  
  DateTime now = rtc.now(); //date & time
  int temp = rtc.getTemperature();

  String filename =  String(now.year()) + String(now.month()) + String(n) + String(".txt");  
  File dataFile = SD.open(filename,FILE_WRITE);
  if (SD.exists(filename)){
    filename[8] += 1;
    Serial.println("exists");
    Serial.println(n);
    String filename =  String(now.year()) + String(now.month()) + String(n) + String(".txt");  
    File dataFile = SD.open(filename,FILE_WRITE);
    Serial.println(filename);
  }
  else{
   Serial.println("not exists");
  }
  
  //File dataFile = SD.open("datalog.txt",FILE_WRITE); //open dataFile datalog.txt
  String userinfo = "In use by: Mena"; //user info
  String actual_date = "Date: " + String(now.year()) + String(now.month()) + String(now.day()); //actual date
  String actual_time = "Time: " + String(now.hour()) + String(now.minute()) + String(now.second()); //actual time
  String infoline_start = "Temperature: " + String(temp) + "°C" + ", Humidity: " +String(humidity); //String(now.year());// file infoline
  String header = "ID, loadcell, strain1, temperature, humidity, runtime"; // file header
  
  if (dataFile) { //if file is available write sensor data
    //dataFile.println(",,"); //blank line in case there where previous data
    dataFile.println(userinfo); //print user info
    dataFile.println(actual_date); //print date
    dataFile.println(actual_time); //print time
    dataFile.println(infoline_start); //printing general info in file
    dataFile.println(header); //writing header in file
    dataFile.close();
    Serial.println(userinfo); //print user info
    Serial.println(actual_date); //print date
    Serial.println(actual_time); //print time
    Serial.println(infoline_start); //print infoline
    Serial.println(header); // print also sensor data to serial
  }
  
  else {
    Serial.println("error opening datalog.txt"); // error message if file not open
  } 
  

}

//-----------------------------------LOOP-------------------------------------------------------------------------
void loop() {
 
  DateTime now = rtc.now(); //date & time
  float loadcellout = loadcell.read(); // reading HX711 from loadcell
  float strain1out = strain1.read(); // reading HX711 from strain gauge 1
  int chk = DHT.read(DHT11_PIN);
  //int temp = DHT.temperature;
  int humidity = DHT.humidity;
  int temp = rtc.getTemperature();
  offsettime = millis();
  String dataoutput = String(id) + ", " + String(loadcellout) + ", " + String(strain1out) + "," + String(temp) + "," + String(humidity) + "," + String(offsettime);


  buttonState = digitalRead(buttonPin); // read state of button 
  
  
if(buttonState != lastButtonState) {//compare current and last button states
    //if state has changed (button pressed)
    if (buttonState == HIGH) {//if button pressed
      buttonPushCounter++; 
    }
    lastButtonState = buttonState;
}
File dataFile = SD.open(filename,FILE_WRITE); //open dataFile 
//File dataFile = SD.open("datalog.txt",FILE_WRITE); // open dataFile datalog.txt
if (buttonPushCounter % 2 == 1) {
    digitalWrite(redledPin, HIGH);
    digitalWrite(greenledPin, LOW);
    dataFile.println(dataoutput); //print sensor data to datafile
    dataFile.close();
    Serial.println(dataoutput); // print also sensor data to serial
    id++; //Increment ID number for row
  } else {
    digitalWrite(redledPin, LOW);
    digitalWrite(greenledPin, HIGH);
}  
  
  //delay(1000);
}
