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


//----------INCLUDING LIBRARIES---------------------------------------------------------------
#include <SPI.h> //lib for serial peripheral interface
#include <SD.h> //lib for sd card
#include <Q2HX711.h> //lib for HX711
//#include "RTClib.h" //lib for timestamp
#include <dht11.h> //lib for temperature & humidity

//----------DEFINING PINS, VARIABLES & FUNCTIONS-----------------------------------------------
const int chipSelect = 4; //port for sd card

//Variables for hx711 
const int DOUT0 = 5; //loadcell data
const int CLK0 = 6; //loadcell clock
const int DOUT1 = 9; //strain gauge 1
const int CLK1 = 10; //strain gauge 1

const int redledPin = 11; //red led pin (data acquisition on going)
const int greenledPin = A5;//green led pin (no data acquisition,system ready)
const int buttonPin = 12; //button pin

int buttonPushCounter = 0; // counter for the number of button presses
int buttonState = 0; //current button state
int lastButtonState = 0; // previous state of the button

#define DHT11_PIN 13 //data pin temperature&humidity

long id = 1; //store the id # of our reading                

//Functions for hx711
Q2HX711 loadcell(DOUT0,CLK0); //loadcell
Q2HX711 strain1(DOUT1,CLK1); //strain gauge 1

//Function for timestamp
//RTC_DS1307 rtc;

//Function for DHT11 (temp&hum)
dht11 DHT;

//----------SETUP LOOP------------------------------------------------------------------------------
void setup() {
  
  Serial.begin(9600); // start serial
  
  //rtc.begin();

  //if(! rtc.isrunning()){
    //Serial.println("RTC is NOT running!"); // RTC not running
    //rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); // setting RTC to date&time this sketch was compiled
  int chk = DHT.read(DHT11_PIN);
  int temp = DHT.temperature;
  int humidity = DHT.humidity;
  
  while (!Serial) {
    ; // wait for serial port connection
  }

  Serial.print("Initializing SD card..."); //initializing sd card

  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed"); // sd card not found
    
    while (1);
  }
  Serial.println("card initialized."); //sd card ok

  pinMode(redledPin, OUTPUT); // define redledPin as output for data acquisition
  pinMode(A0, OUTPUT);
  pinMode(greenledPin,OUTPUT); //define greenledPin as output for system ready
  pinMode(buttonPin, INPUT); // define buttonPin as input
  

  File dataFile = SD.open("datalog.txt",FILE_WRITE); //opening .csv file in writing mode
  String userinfo = "In use by: Mena"; //user info
  String infoline = String(temp) + String(humidity);// file infoline
  String header = "ID, loadcell, strain1, temperature, humidity"; // file header
  
  if (dataFile) { //if file is available write sensor data
    //dataFile.println(",,"); //blank line in case there where previous data
    dataFile.println(userinfo); //print user info
    //dataFile.println(infoline); //printing general info in file
    dataFile.println(header); //writing header in file
    dataFile.close();
    Serial.println(header); // print also sensor data to serial
  }
  
  else {
    Serial.println("error opening datalog.txt"); // error message if file not open
  } 
  

}

//-----------------------------------LOOP-------------------------------------------------------------------------
void loop() {
 
  //DateTime time = rtc.now(); //date & time
  
  float loadcellout = loadcell.read(); // reading HX711 from loadcell
  float strain1out = strain1.read(); // reading HX711 from strain gauge 1
  int chk = DHT.read(DHT11_PIN);
  int temp = DHT.temperature;
  int humidity = DHT.humidity;
  String dataoutput = String(id) + ", " + String(loadcellout) + ", " + String(strain1out) + "," + String(temp) + "," + String(humidity);

  //File dataFile = SD.open(String("datalog\t") + time.timestamp(DateTime::TIMESTAMP_FULL)+String(".txt"), FILE_WRITE); //open file on sd card and name 

  buttonState = digitalRead(buttonPin); // read state of button 
  File dataFile = SD.open("datalog.txt",FILE_WRITE); // open dataFile for writing sensor values
  
if(buttonState != lastButtonState) {//compare current and last button states
    //if state has changed (button pressed)
    if (buttonState == HIGH) {//if button pressed
      buttonPushCounter++; 
    }
    lastButtonState = buttonState;
}

if (buttonPushCounter % 2 == 1) {
    digitalWrite(redledPin, HIGH);
    digitalWrite(greenledPin, LOW);
    dataFile.println(dataoutput); //print sensor data to datafile
    Serial.println(dataoutput); // print also sensor data to serial
    id++; //Increment ID number for row
  } else {
    digitalWrite(redledPin, LOW);
    digitalWrite(greenledPin, HIGH);
}  
  
  //delay(1000);
}
