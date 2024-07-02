import processing.serial.*;
int pos = 0;


Serial myPort;
String receiver;

boolean new_round = false;


void setup(){
  size(600, 600);
  background(0, 0, 0);
  myPort = new Serial(this, "COM3", 9600);
}


void draw(){
  if ( myPort.available() > 0) {  // If data is available,
    receiver = myPort.readStringUntil('\n');
  }
  textSize(30);
  text("Vorgabe: ", 30, 150);
  textSize(30);
  text("Distanz: ", 30, 100);
  if (receiver.trim() == "N"){
    if ( myPort.available() > 0) {  // If data is available,
    receiver = myPort.readStringUntil('\n');
    }
    pos = 0;
    for(int i = 0; i < Integer.parseInt(receiver.trim()); i++){
          pos = pos + 15;
          fill(255, 255, 255);
          rect(160 + pos, 120, 10, 40);
        }
    delay(1000);
    for(int i = 0; i < Integer.parseInt(receiver.trim()); i++){
          pos = pos + 15;
          fill(0, 0, 0);
          rect(160 + pos, 120, 10, 40);
        }
    myPort.write("W");
    new_round = false;
  }else{
    if ( myPort.available() > 0) {  // If data is available,
    receiver = myPort.readStringUntil('\n');
    }
    
    if(receiver.trim() == "L"){
      textSize(30);
      text("LOST", 175, 70);
      while(true){
        textSize(30);
        text("LOST", 175, 70);
      }
    }else if(receiver.trim() == "C"){
      textSize(30);
      text("Correct", 175, 70);
      delay(1000);
      myPort.write("W");
    }
    if(receiver != null && receiver.trim() != ""){
      pos = 0;
      for(int i = 0; i < Integer.parseInt(receiver.trim()); i++){
        pos = pos + 15;
        fill(255, 255, 255);
        rect(160 + pos, 70, 10, 40);
      }
    }
  }
}
