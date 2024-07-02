import processing.serial.*;

Serial myPort = new Serial(this, "COM8", 9600);
String distance;
String angle;
double x;
double y;
float x_r;
float y_r;
void setup(){
  
  size(600, 600);
  background(0, 0, 0);
}

void draw(){
  if ( myPort.available() > 0) {  
    distance = myPort.readStringUntil('\n');
  }
  myPort.write("1");
  if ( myPort.available() > 0) {  
    angle = myPort.readStringUntil('\n');
  }
  myPort.write("2");
  
  fill(255, 255, 255);
  circle(300, 100, 15);
  
  x = Math.cos(45) + 300;
  y = Math.sin(200) + 100;
  
  x_r = (float) x;
  y_r = (float) y;
  
  fill(0, 0, 255);
  println(x_r);
  println(y_r);
  circle(x_r + 100, y_r + 100, 20);
}
