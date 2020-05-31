#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <HX711.h>

String DEV_ID = "PAT00001";                                   //Input the device id here
const char *ssid = "Westeros";                                 //ENTER YOUR WIFI SETTINGS
const char *password = "webpass123";

//Web/Server address to read/write from 
const char *host = "192.168.0.102"; 
String Link = "http://192.168.0.102:8000/receive/";

int critical_value = 20;
int very_critical_value = 10;
const int SCALE_DOUT_PIN = D6;
const int SCALE_SCK_PIN = D5;
const int Buzzer = D8;
const int LED = D7;
const int Push_button = D3;
int push_button_state = 0;

int flag = 0;
float initial_saline_weight;
float weight = 0;
int count = 0;

int sendPercentage=100;
int previous_sendPercentage =0;
String payload;
float full_bag_weight;
float package_weight;

void buzzer_alarm(int rate);        // input how many times to beep in a second
void buzzer_stop();
void buzzer_indication(int times, int Delay);  //input how many times to beep buzzer and stop

HX711 scale(SCALE_DOUT_PIN, SCALE_SCK_PIN);

//=======================================================================
//                    Power on setup
//=======================================================================

void setup() {
  Serial.begin(115200);
  scale.set_scale(45);// <- set here calibration factor!!!
  scale.tare();
  pinMode(Buzzer,OUTPUT);
  pinMode(LED,OUTPUT);
  pinMode(Push_button,INPUT_PULLUP);
  
  digitalWrite(Buzzer,HIGH);
  digitalWrite(LED,HIGH);
  delay(1000);
  digitalWrite(Buzzer,LOW);
  digitalWrite(LED,LOW);

   
  weight = scale.get_units(1);
  float new_weight = 0;
  int not_ok = 1;
  

  //Wait and slow beepiing untill saline is On device hook
  Serial.println("Waiting for saline.....");
 
  while(true)
  {
    new_weight = scale.get_units(1);
    if(abs(new_weight-weight) >250)break;   //250 depends on variety of saline pack can be used in this device
    buzzer_indication(1,1000);
    weight = new_weight;
  }
Serial.println("Saline on device");
weight = 0;

Serial.println("Saline recognizing...");
//automatic weight recognition
  while(true)
  {
    new_weight = abs(scale.get_units(1));
    Serial.println(new_weight);
    if(abs(new_weight-weight) <10 && count>=15)
    {
      if(new_weight > 300 && new_weight < 800)
      {
          initial_saline_weight = 500;          
          //not_ok = 0;
          break;
      }
      else if(new_weight > 800 && new_weight < 1500)
      {
          initial_saline_weight = 1000;
          //not_ok = 0;
          break;
      }
    }
    weight = new_weight;
    count++;
  }
  count=0;
Serial.println("Saline recognized as "+ String(initial_saline_weight));
  


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


  full_bag_weight = abs(scale.get_units(1));
  package_weight = abs(full_bag_weight - initial_saline_weight);
  Serial.println("full_bag_weight: "+ String(full_bag_weight));
  Serial.println("package_weight: "+ String(package_weight));
  buzzer_stop();
}

//=======================================================================
//                    Main Program Loop
//=======================================================================




void loop() {

  weight = abs(scale.get_units(1)) - package_weight;
  Serial.println("Weight: "+ String(weight, 2));
  
  HTTPClient http;    //Declare object of class HTTPClient

 //GET Data
  
  sendPercentage= (weight/initial_saline_weight)*100 ;
  if(sendPercentage<0)sendPercentage=0;
  if(sendPercentage>100)sendPercentage=100;
  
Serial.println(sendPercentage);

  String postData = DEV_ID + "," + String(sendPercentage);
  Serial.print(postData);
  Serial.print(Link);
  http.begin(Link);     //Specify request destination
  
  int httpCode = http.POST(postData);            //Send the request
  payload = http.getString();    //Get the response payload                         //6 for mute commad, 5 for not mute button pressed

  Serial.println(httpCode);   //Print HTTP return code
  Serial.println("payload" + payload);    //Print request response payload
  http.end();  //Close connection


/*
//debugging
if (sendPercentage <=critical_value && very_critical_value<sendPercentage)
{
  Serial.println("State : Critical");
}
else if (sendPercentage <=very_critical_value)
{
  Serial.println("State : Very Critical");
}
else
{
  Serial.println("State : Normal");
}
*/

//push_button_state change for entering 1-10% zone from 11-20% zone
if ((previous_sendPercentage <=critical_value  && previous_sendPercentage >very_critical_value) && (sendPercentage<=very_critical_value))
{
  push_button_state = 0;
}
previous_sendPercentage=sendPercentage;


//Push button read
  int button = digitalRead(Push_button);    // it gives 0 for press, 1 otherwise
  if (button == 0)Serial.println("button pressed");
  if((sendPercentage <= critical_value) && (button == 0 || payload == "1"))push_button_state = 1;   //when percentage under critical and mute button pressed
  //Serial.println(push_button_state);                                                              //payload returns 1 if mute button pressed
  Serial.println("\n\n");

  
//critical and very_critical saline level indication
  if (push_button_state == 0)
  {
    count++;
    if(sendPercentage <= critical_value  && very_critical_value < sendPercentage  && count>  8)
      {
        buzzer_indication(1,500);
        count = 0;
      }
    else if(sendPercentage <= very_critical_value  && count>  4)
      {
        buzzer_indication(2,250);
        count = 0;
      }
  }
if (sendPercentage >=critical_value)
{
  delay(1000);
  push_button_state = 0;
}
  
}
//=======================================================================


void buzzer_alarm(int rate){
  digitalWrite(Buzzer,HIGH);
  delay(500/rate);
  digitalWrite(Buzzer,LOW );
  delay(500/rate);
}

void buzzer_stop(){
 digitalWrite(Buzzer,LOW );
}
void buzzer_indication(int times, int Delay){
  for( int i=0;i<times;i++)
  {
    digitalWrite(Buzzer,HIGH);
    digitalWrite(LED,HIGH);
    delay(Delay);
    digitalWrite(Buzzer,LOW );
    digitalWrite(LED,LOW );
    delay(Delay);
  }
}
