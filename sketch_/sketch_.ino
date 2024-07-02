
#include <Servo.h>

int trigger = 6;
int echo = 7;


Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

char val;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo objecSer
  Serial.begin(9600);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
}

int entfernung(){
    digitalWrite(trigger, 1);
    delay(15);
    digitalWrite(trigger, 0);
    long entfernung = (pulseIn(echo, 1)/2) * 0.03432;
    return round(entfernung);

}

void loop() {
  myservo.write(0);
  delay(15);
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);
    if (entfernung() < 100){
      Serial.println(entfernung());
      while(true){
        if(Serial.available()){
          val = Serial.read();
          if(val == "1"){
            break;
          }
        }
      }
      Serial.println(pos);
      while(true){
        if(Serial.available()){
          val = Serial.read();
          if(val == "2"){
            break;
          }
        }
      }
    }
    
    delay(50);
  }
}