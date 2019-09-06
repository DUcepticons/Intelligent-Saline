 /*
 * HTTP Client GET Request
 * Copyright (c) 2018, circuits4you.com
 * All rights reserved.
 * https://circuits4you.com 
 * Connects to WiFi HotSpot. */

#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <HX711.h>

/* Set these to your desired credentials. */
const char *ssid = "Niloy";  //ENTER YOUR WIFI SETTINGS
const char *password = "1q2w3e4r5t6Y";

//Web/Server address to read/write from 
const char *host = "192.168.0.12";  

// Scale Settings
const int SCALE_DOUT_PIN = D5;
const int SCALE_SCK_PIN = D6;

HX711 scale(SCALE_DOUT_PIN, SCALE_SCK_PIN);

//=======================================================================
//                    Power on setup
//=======================================================================

void setup() {
  delay(1000);
  Serial.begin(115200);
  WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  scale.set_scale(310);// <- set here calibration factor!!!
  scale.tare();
  }

  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP
}

//=======================================================================
//                    Main Program Loop
//=======================================================================
int sendPercentage=100;

void loop() {
  float saline_bag_weight=1000;
  float weight = scale.get_units(1);
  Serial.println(String(weight, 2));
  
  HTTPClient http;    //Declare object of class HTTPClient

  String   Link;


  //GET Data
  
  sendPercentage= (weight/saline_bag_weight)*100 ; 
  if(sendPercentage<0)
  {
    sendPercentage=0;
  }
  if(sendPercentage>100)
  {
    sendPercentage=100;
  }  
  Link = "http://192.168.0.105:8000/receive/";
  String postData = "7,2,5," + String(sendPercentage);
  Serial.print(Link);
  http.begin(Link);     //Specify request destination
  
  int httpCode = http.POST(postData);            //Send the request
  String payload = http.getString();    //Get the response payload

  Serial.println(httpCode);   //Print HTTP return code
  Serial.println(payload);    //Print request response payload

  http.end();  //Close connection
  
  delay(2000);  //GET Data at every 5 seconds
}
//=======================================================================
