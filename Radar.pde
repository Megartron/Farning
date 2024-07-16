import processing.serial.*;

Serial myPort = new Serial(this, "COM8", 9600);
String receive;
double distance;
double angle;
double x;
double y;
float x_r;
float y_r;
void setup(){
  
  size(600, 600);
  background(0, 0, 0);
}

float position_x(double x, double degree, double distance){
  double radian = Math.toRadians(degree);
  double r = Math.cos(radian);
  
  double x_new =  x + distance*r;
  
  return (float) x_new;
}

float position_y(double y, double degree, double distance){
  double radian = Math.toRadians(degree);
  double r = Math.sin(radian);
  double y_new = y + distance*r;
  
  return (float) y_new;
}

void draw(){
  receive = "";
  for(int i = 0; i < 10; i++){
    
    noFill();
    stroke(#00ff00);
    arc(300, 100, 500 - i * 50, 500 - i * 50, radians(0), radians(180));
  }
  line(50, 100, 550, 100);
  
  
  
  if ( myPort.available() > 0) {  
    receive = myPort.readStringUntil('\n');
  }
  print("distance: ");
  println(receive);
  if (receive != null && receive.trim() != ""){
    
    distance = Double.parseDouble(receive.trim());
    receive = "";
    
    if ( myPort.available() > 0) {  
      receive = myPort.readStringUntil('\n');
    }
    print("angle: ");
    println(receive);
    delay(35);
    if (receive != null && receive.trim() != ""){
      angle = Double.parseDouble(receive.trim());
      
      fill(255, 255, 255);
      circle(300, 100, 15);
      
      float circle_x = position_x(300, angle, distance/2);
      float circle_y = position_y(100, angle, distance/2);
    
      
      
      fill(0, 0, 255);
    
      circle(circle_x, circle_y, 20);
    }
  }
}
