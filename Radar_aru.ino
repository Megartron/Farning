#include <Servo.h>
Servo myservo;
int pos;
int echo = 7;
int trigger = 6;
long entfernung = 0;
char val = "n";

void setup() {
  // put your setup code here, to run once:
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600);
  myservo.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:

  for (pos = 0; pos <= 180; pos += 1) {
  // in steps of 1 degree
    /*while(true){
      if (Serial.available()){
        if(Serial.read() == "1"){
          break;
        } 
      }
    }*/
  val = "n";
  myservo.write(pos);              
  delay(15);
  digitalWrite(trigger, 1);
    delay(10);
    digitalWrite(trigger, 0);
    entfernung = (pulseIn(echo, 1)/2) * 0.03432;
    if (entfernung <= 100){
      Serial.println(entfernung);
      delay(10);
    }else{
      Serial.println("");
      delay(10);
    }
    /*while(true){
      if (Serial.available()){
        if(Serial.read() == "1"){
          break;
        } 
      }
    }*/
    Serial.println(pos);
    delay(10);
    val = "n";
    
  }
}
    
