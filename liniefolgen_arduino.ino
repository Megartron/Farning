
#define rechts_v 5
#define links_v 6
#define rechts_motor 7
#define links_motor 8
#define start 3
#define sensor_l A0
#define sensor_r A2
#define sensor_m A1


int i = 0;
int letzer_turn = 0;

int v_normal = 50;
int v_bremsen = 0;

int anzahl_r = 0;
int anzahl_l = 0;
int kontrolle = 0;


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
  analogWrite(links_v, v_bremsen);
  analogWrite(rechts_v, v_normal);
  
  while (farbe_mitte != LOW){
    farbe_mitte = (analogRead(sensor_m) > 500) ? LOW : HIGH;
  }

  letzer_turn = -1;
}

void rechts_suchen(){
  int farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
  digitalWrite(rechts_motor, LOW);
  analogWrite(links_v, v_normal);
  analogWrite(rechts_v, v_bremsen);
  
  while (farbe_mitte != LOW){
    farbe_mitte = (analogRead(sensor_m) > 500) ? LOW : HIGH;
  }

  letzer_turn = 1;
}


void loop(){ //--------------------------------------------------------------------------------------------------------------
  int farbe_links = (analogRead(sensor_l) > 500) ? LOW : HIGH;
  int farbe_mitte = (analogRead(sensor_m) >  500) ? LOW : HIGH;
  int farbe_rechts = (analogRead(sensor_r) > 500) ? LOW : HIGH;

  digitalWrite(rechts_motor, HIGH);
  digitalWrite(links_motor, HIGH);

  if (farbe_links == LOW && farbe_rechts == LOW && farbe_mitte == LOW) {
    digitalWrite(rechts_motor, HIGH);
    digitalWrite(links_motor, LOW);
    analogWrite(links_v, 60);
    analogWrite(rechts_v, 60);
    delay(75);
    int t = 1;
    analogWrite(links_v, 0);
    analogWrite(rechts_v, 0);
    while(farbe_links == LOW && farbe_rechts == LOW && farbe_mitte == LOW){
      if(t % 2 == 0){
        digitalWrite(rechts_motor, LOW);
        digitalWrite(links_motor, HIGH);
      }else{
        digitalWrite(rechts_motor, HIGH);
        digitalWrite(links_motor, LOW);
      }
      analogWrite(links_v, 60);
      analogWrite(rechts_v, 60);
      delay(t * 150);
      analogWrite(links_v, 0);
      analogWrite(rechts_v, 0);
      t++;
    }
  }
  else if (farbe_links == LOW && farbe_rechts == HIGH){
    kontrolle = 50;
    anzahl_r = 0;
    anzahl_l = 0;
    Serial.println("l");
    rechts_suchen();
  }

  else if (farbe_links == HIGH && farbe_rechts == LOW){
    kontrolle = 50;
    anzahl_r = 0;
    anzahl_l = 0;
    Serial.println("r");
    links_suchen();

  }
  else if (farbe_mitte == LOW){
    kontrolle = 50;
    anzahl_r = 0;
    anzahl_l = 0;
    Serial.println("m");
    analogWrite(links_v, v_normal);
    analogWrite(rechts_v, v_normal);
  

  }else{
    kontrolle = 50;
    anzahl_r = 0;
    anzahl_l = 0;

    Serial.println("keine linie");

    if(letzer_turn == 1){
      rechts_suchen();

    } else {
      links_suchen();
    }
  }
  delay(10);
}

/*#include <Servo.h>
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
float distance = 100;

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

void drehen(int r){
  digitalWrite(rechts_motor, 1);
  digitalWrite(links_motor, 1);

  if(r == 0){
    analogWrite(links_v, 0);
    analogWrite(rechts_v, 70);
  }else{
    analogWrite(links_v, 70);
    analogWrite(rechts_v, 0);
  }
  delay(1400);
  set_v(0);
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
  


  if(distance <= 20){
    set_v(0);
    for (int angle = 50; angle >= 1; angle--) {
      servo.write(angle);
      delay(10);  // Adjust to go slower or faster
    }
    float rechts_dis = dis();
    Serial.print(rechts_dis);

    for (int angle = 120; angle <= 179; angle++) {
      servo.write(angle);
      delay(10);  // Adjust to go slower or faster
    }
    float links_dis = dis();
    Serial.print(links_dis);

    Serial.print("-------------------");




    if(links_dis < rechts_dis){
      drehen(1);
      for (int angle = 120; angle <= 179; angle++) {
        servo.write(angle);
        delay(10);  // Adjust to go slower or faster
      }

      digitalWrite(rechts_motor, 1);
      digitalWrite(links_motor, 1);
      set_v(60);
      float dist = dis();
      while(dist < 25){
        dist = dis();
      }
      delay(700);
      set_v(0);
      drehen(0);



    }else{
      drehen(0);
      for (int angle = 50; angle >= 1; angle--) {
        servo.write(angle);
        delay(10);  // Adjust to go slower or faster
      }

      digitalWrite(rechts_motor, 1);
      digitalWrite(links_motor, 1);
      set_v(60);
      float dist = dis();
      while(dist < 25){
        dist = dis();
      }
      delay(700);
      set_v(0);
      drehen(1);
    }

  }else{
    digitalWrite(rechts_motor, HIGH);
    digitalWrite(links_motor, HIGH);
    set_v(50);
  }

  distance = dis();

  delay(100);
} */
