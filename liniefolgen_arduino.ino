#include <TaskScheduler.h>

#define rechts_v 5
#define links_v 6
#define rechts_motor 7
#define links_motor 8
#define start 3
#define sensor_l A0
#define sensor_r A2
#define sensor_m A1

Scheduler runner;
int i = 0;
int letzer_turn = 0;


void schlange();

//Task finden(10, TASK_FOREVER, &linie_kontrollieren);


void setup(){
  Serial.begin(9600);
  pinMode(rechts_v, OUTPUT);
  pinMode(links_v, OUTPUT);
  pinMode(rechts_motor, OUTPUT);
  pinMode(links_motor, OUTPUT);
  pinMode(start, OUTPUT);

  pinMode(sensor_l, INPUT);
  pinMode(sensor_m, INPUT);
  pinMode(sensor_r, INPUT);

  unsigned long startTime = millis();

  digitalWrite(start, HIGH);
}

void links_suchen(){
  int farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
  digitalWrite(links_motor, LOW);
  analogWrite(links_v, 20);
  analogWrite(rechts_v, 50);
  
  while (farbe_mitte != LOW){
    farbe_mitte = (analogRead(sensor_m) > 400) ? LOW : HIGH;
  }

  letzer_turn = -1;
}

void rechts_suchen(){
  int farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
  digitalWrite(rechts_motor, LOW);
  analogWrite(links_v, 50);
  analogWrite(rechts_v, 20);
  
  while (farbe_mitte != LOW){
    farbe_mitte = (analogRead(sensor_m) > 400) ? LOW : HIGH;
  }

  letzer_turn = 1;
}

void linie_kontrollieren(){

}


void linie_finden(){
  analogWrite(links_v, 50);
  analogWrite(rechts_v, 20);
  int i = 0;
  
  while (true){    
    analogWrite(links_v, 30);
    analogWrite(rechts_v, 30);
    int farbe_links = (analogRead(sensor_l) > 500) ? LOW : HIGH;
    int farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
    int farbe_rechts = (analogRead(sensor_r) > 500) ? LOW : HIGH;

    if (farbe_links == LOW || farbe_rechts == LOW || farbe_mitte == LOW){
      analogWrite(links_v, 0);
      analogWrite(rechts_v, 0);
    
      if (farbe_links == LOW || farbe_rechts == LOW || farbe_mitte == LOW){
        return;
      }
    }
  }
}


void loop(){ //--------------------------------------------------------------------------------------------------------------
  int farbe_links = (analogRead(sensor_l) > 500) ? LOW : HIGH;
  int farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
  int farbe_rechts = (analogRead(sensor_r) > 500) ? LOW : HIGH;

  digitalWrite(rechts_motor, HIGH);
  digitalWrite(links_motor, HIGH);

  if (farbe_mitte == LOW){
    Serial.println("m");
    analogWrite(links_v, 50);
    analogWrite(rechts_v, 50);
  }

  else if (farbe_links == LOW && farbe_rechts == HIGH){
    Serial.println("l");
    rechts_suchen();
  }

  else if (farbe_links == HIGH && farbe_rechts == LOW){
    Serial.println("r");
    links_suchen();

  }else{

    Serial.println("keine linie");

    if(letzer_turn == 1){
      digitalWrite(rechts_motor, LOW);
      analogWrite(links_v, 50);
      analogWrite(rechts_v, 20);

    } else {
      digitalWrite(links_motor, LOW);
      analogWrite(links_v, 20);
      analogWrite(rechts_v, 50);

    }
    
    while (farbe_mitte != HIGH){

      if (farbe_links == LOW && farbe_rechts == HIGH){
        Serial.println("l");
        rechts_suchen();
      }

      else if (farbe_links == HIGH && farbe_rechts == LOW){
        Serial.println("r");
        links_suchen();
      }
      farbe_links = (analogRead(sensor_l) > 500) ? LOW : HIGH;
      farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
      farbe_rechts = (analogRead(sensor_r) > 500) ? LOW : HIGH;
    }
  }
  delay(100);
}



/* AUFGABE 3
  #include <Servo.h>
#define rechts_v 5
#define links_v 6
#define rechts_motor 7
#define links_motor 8
#define start 3
#define sensor_l A0
#define sensor_r A2
#define sensor_m A1

#define TRIG_PIN 13
#define ECHO_PIN 12

int t = 1500;
Servo servo;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(rechts_v, OUTPUT);
  pinMode(links_v, OUTPUT);
  pinMode(rechts_motor, OUTPUT);
  pinMode(links_motor, OUTPUT);
  pinMode(start, OUTPUT);

  pinMode(sensor_l, INPUT);
  pinMode(sensor_m, INPUT);
  pinMode(sensor_r, INPUT);

  servo.attach(10);

  unsigned long startTime = millis();

  digitalWrite(rechts_motor, HIGH);
  digitalWrite(links_motor, HIGH);
  digitalWrite(start, HIGH);
}

void set_v(int v){
  analogWrite(links_v, v);
  analogWrite(rechts_v, v);
}

float dis(){
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read the echo time
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate distance in cm
  float distance = duration * 0.0343 / 2;
  return distance;
}

void loop() {
  servo.write(90);
  
  float distance = dis();

  if(distance <= 15){
    set_v(0);
    for (int angle = 90; angle >= 45; angle--) {
      servo.write(angle);
      delay(15);  // Adjust to go slower or faster
    }
    float rechts_dis = dis();
    Serial.print(rechts_dis);

    for (int angle = 90; angle <= 135; angle++) {
      servo.write(angle);
      delay(15);  // Adjust to go slower or faster
    }
    float links_dis = dis();
    Serial.print(links_dis);

    Serial.print("-------------------");

    if(links_dis < rechts_dis){
      analogWrite(links_v, 50);
      analogWrite(rechts_v, 0);

      delay(t);
      set_v(70);
      delay(700);

      analogWrite(links_v, 0);
      analogWrite(rechts_v, 50);

      delay(t);
    }else{
      analogWrite(links_v, 0);
      analogWrite(rechts_v, 50);

      delay(t);
      set_v(70);
      delay(700);

      analogWrite(links_v, 50);
      analogWrite(rechts_v, 0);

      delay(t);
    }

    

  }else{
    set_v(50);
  }

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");


  delay(500);
}
*/

