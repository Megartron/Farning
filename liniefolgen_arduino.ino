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

void loop(){
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