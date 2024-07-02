
int echo = 6;
int trigger = 7;
long entfernung = 0;
int display = 0;
int memory[20];
int j = 0;
int k = 0;
int randNum = 0;
const int buttonPin = 2;
bool weiter = False

void setup() {
  // put your setup code here, to run once:
  pinMode(buttonPin, INPUT);
  long seed = analogRead(A0) + analogRead(A1) + analogRead(A3) + micros();
  randomSeed(seed);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  Serial.begin(9600);
  delay(1000);
}



void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("N")
  randNum = round(random(0, 21)) + 1;
  Serial.println(randNum);
  while(!weiter){
    if (Serial.available() > 0){
      char receiver = Serial.read();
      if(receiver == "W"){
        weiter = true;
      }
    }
  }
  weiter = false;
  memory[j] = randNum;
  k = 0;
  while(memory[k != 0]){
    digitalWrite(trigger, 1);
    delay(10);
    digitalWrite(trigger, 0);
    entfernung = round((pulseIn(echo, 1)/2) * 0.03432);
    display = round(entfernung/5) + 1;
    Serial.println(display);

    if (digitalRead(buttonPin) == HIGH) {
      if (display != memory[k]){
        while(true){
          Serial.println("L");
          delay(10000);
        }
      }else{
        Serial.println("C");
        k++;
        while(!weiter){
          if (Serial.available() > 0){
            char receiver = Serial.read();
            if(receiver == "W"){
              weiter = true;
            }
          }
        }
        weiter = false;
      }
    }
  }
}









