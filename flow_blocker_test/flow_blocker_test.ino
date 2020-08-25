#include<Servo.h> 
 Servo servo;
 int i;
 void setup() 
{
 servo.attach(6);
 
}
void Lock(int Speed, int Delay);
void Open(int Speed, int Delay);
void loop() {

  Lock(110, 4500);
  delay(1000);
  Open(70, 4500);
  delay(1000);
  
}

void Lock(int Speed, int Delay){
  servo.write(Speed);
  delay(Delay);
  servo.write(90);
}

void Open(int Speed, int Delay){
  servo.write(Speed);
  delay(Delay);
  servo.write(90);
}
