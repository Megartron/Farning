#include <Wire.h>
#include <LiquidCrystal_I2C.h>

byte block[] = {
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111
};

byte rect[] = {
  B11111,
  B10001,
  B10001,
  B10001,
  B10001,
  B10001,
  B10001,
  B11111
};

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);
int echo = 6;
int trigger = 7;
long entfernung = 0;
int display = 0;
int memory[20];
int j = 0;
int k = 0;
int randNum = 0;
const int buttonPin = 2;
void setup() {
  // put your setup code here, to run once:
  pinMode(buttonPin, INPUT);
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, block);
  lcd.createChar(1, rect);
  long seed = analogRead(A0) + analogRead(A1) + analogRead(A3) + micros();
  randomSeed(seed);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600);
}

void loop() {
  lcd.clear();
  for (int l = 0; l < 10; l++){
    lcd.setCursor(l, 1);
    lcd.print(l);
  }
  for (int l = 0; l < 6; l++){
    lcd.setCursor(l + 10, 1);
    lcd.print(l);
  }

  randNum = round(random(0, 16)) + 1;
  Serial.println(randNum);
  for (int i = 0; i < randNum; i++) {
  lcd.setCursor(i, 0);
  lcd.write(1);
}
  memory[j] = randNum;
  delay(2000);
  k = 0;
  while(memory[k] != 0){

    Serial.println(memory[k]);
    lcd.clear();
    digitalWrite(trigger, 1);
    delay(10);
    digitalWrite(trigger, 0);
    entfernung = (pulseIn(echo, 1)/2) * 0.03432;
    display = round(entfernung/5) + 1;

    for (int l = 0; l < 10; l++){
    lcd.setCursor(l, 1);
    lcd.print(l);
  }
  for (int l = 0; l < 6; l++){
    lcd.setCursor(l + 10, 1);
    lcd.print(l);
  }

    Serial.print("Entfernung: ");
    Serial.println(entfernung);
    Serial.print("Display: ");
    Serial.println(display);
    if (display <= 16){
      for (int i = 0; i < display; i++) {
      lcd.setCursor(i, 0);
      lcd.write(block);
    }
    
    }
    if (digitalRead(buttonPin) == HIGH) {
      // turn LED on:
      if (display != memory[k]){
        while(true){
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("YOU LOST!");
          lcd.setCursor(0, 1);
          lcd.print("Your distance:");
          lcd.setCursor(14, 1);
          lcd.print(display);
          delay(3000);
          lcd.clear();
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("YOU LOST!");
          lcd.setCursor(0, 1);
          lcd.print("True distance:");
          lcd.setCursor(14, 1);
          lcd.print(memory[k]);
          delay(3000);
        }
      }else{
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Correct!");
        delay(1000);
        k++;
      }
    }
    delay(100);
    
  }
  j++;
  

 
}
