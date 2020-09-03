#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <HX711.h>

/* Set these to your desired credentials. */
const char *ssid = "Inan Afra";  //ENTER YOUR WIFI SETTINGS
const char *password = "afra2017";

//Web/Server address to read/write from 
const char *host = "192.168.0.101";  

#define critical_value  20
const int SCALE_DOUT_PIN = D6;
const int SCALE_SCK_PIN = D5;

const int Buzzer = D8;
const int LED = D7;

int flag = 0;
float saline_bag_weight=1000;
float weight = 0;

HX711 scale(SCALE_DOUT_PIN, SCALE_SCK_PIN);

//=======================================================================
//                    Power on setup
//=======================================================================

void setup() {
  scale.set_scale(45);// <- set here calibration factor!!!
  scale.tare();
  
  pinMode(Buzzer,OUTPUT);
  pinMode(LED,OUTPUT);
  digitalWrite(Buzzer,HIGH);
  digitalWrite(LED,HIGH);
  delay(1000);
  digitalWrite(Buzzer,LOW);
  digitalWrite(LED,LOW);
  
  Serial.begin(115200);
  WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    flag ^= 1;
    digitalWrite(Buzzer,flag);
    Serial.print(".");
  }

  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP
  saline_bag_weight=1000;
  weight = scale.get_units(1);
  float new_weight = 0;
  int not_ok = 1;
  int count = 0;
  
  while(not_ok)
  {
    new_weight = scale.get_units(1);
    if(abs(new_weight-weight) <10 && count>=100)
    {
      if(new_weight > 300 && new_weight < 600)
      {
          saline_bag_weight = 500;
          not_ok = 0;
          break;
      }
      else if(new_weight > 700 && new_weight < 1100)
      {
          saline_bag_weight = 1000;
          not_ok = 0;
          break;
      }
    }

    weight = new_weight;
    count++;
  }
  
  
}

//=======================================================================
//                    Main Program Loop
//=======================================================================
int sendPercentage=100;

void loop() {

  weight = scale.get_units(1);

  Serial.println(String(-weight, 2));
  
  HTTPClient http;    //Declare object of class HTTPClient

  String   Link;


  //GET Data
  
  sendPercentage= (-weight/saline_bag_weight)*100 ; 
  if(sendPercentage<0)
  {
    sendPercentage=0;
  }
  if(sendPercentage>100)
  {
    sendPercentage=100;
  }
  if(sendPercentage< critical_value)digitalWrite(Buzzer,HIGH);    
  else
  {
  digitalWrite(Buzzer,LOW);
  }
  Link = "http://192.168.0.101:8000/receive/";
  String postData = "PAT00002," + String(sendPercentage);
  Serial.print(Link);
  http.begin(Link);     //Specify request destination
  
  int httpCode = http.POST(postData);            //Send the request
  String payload = http.getString();    //Get the response payload

  Serial.println(httpCode);   //Print HTTP return code
  //Serial.println(payload);    //Print request response payload

  http.end();  //Close connection
  
  delay(1000);  //GET Data at every 5 seconds
}
//=======================================================================
