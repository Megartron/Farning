import processing.serial.*;
int pos = 0;
int a = 0;
int j = 0;
int dis = 0;
Serial myPort;  // Create object from Serial class
String distance;
void setup(){
  size(600, 600);
  myPort = new Serial(this, "COM8", 9600);
}

void draw(){
  if ( myPort.available() > 0) {  // If data is available,
  distance = myPort.readStringUntil('\n');
  }
  if(distance == "You lost!"){
    text(distance, 30, 100);
    while(true){
      text(distance, 30, 100);
    }
    
  } else if(distance == "Correct!"){
    text(distance, 30, 100);
    while(true){
      if(mousePressed){
        break;
      }
    }
  }
  
  dis = Integer.parseInt(distance);
  textSize(30);
  text("Distance: ", 30, 100);
  pos = 0;
  if(dis <= 20){
    for(int i = 0; i < dis; i++){
      pos = pos + 15;
      fill(0, 0, 0);
      rect(160 + pos, 70, 10, 40);
    }
  }
  for(int i = 0; i < 20; i++){
      pos = pos + 15;
      fill(255, 255, 255);
      rect(160 + pos, 70, 10, 40);
  }
}
