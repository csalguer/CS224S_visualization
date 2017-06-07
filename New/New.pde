ArrayList<Starlet> starlets = new ArrayList<Starlet>();
int width = 1600;
int height = 800;
int offset = 10;
int count = 1;
int rate = 1;
Starlet current_starlet = null;
float lover_one_new_x = 0;
float lover_one_new_y = 0;
float lover_one_previous_x = width/10;
float lover_one_previous_y = height;
float lover_two_new_x = 0;
float lover_two_new_y = 0;
float lover_two_previous_x = width - width/10;
float lover_two_previous_y = height;
int pulse = 120;
int heart_size = 0;
boolean flag = true;
float diameter = 300;
float current_radians = 0;
float chance = 0;
int willingness = 1;

void settings() {
  width = 2560;
  height = 1500;
  size(width, height, P3D);
}

void setup() {
  lover_one_previous_x = width/10;
  lover_one_previous_y = height;
  lover_two_previous_x = width - width/10;
  lover_two_previous_y = height;
  strokeWeight(2);
  for(int i = offset; i < width - offset; i += 25) {
    for(int j = offset; j < height - offset; j += 25) {
      Starlet starlet = new Starlet(new PVector(i+random(-5,5), j+random(-5,5)));
      starlets.add(starlet);
    }
  }
}

void draw() {
  //background(0);
  fill(0,0,0,10);
  noStroke();
  fill(0,0,0,10);
  rect(0,0,width,height);
  if (count % 300 == 0) {
    count = 1;
    flag = true;
    lover_one_previous_x = lover_one_new_x;
    lover_one_previous_y = lover_one_new_y;
    lover_two_previous_x = lover_two_new_x;
    lover_two_previous_y = lover_two_new_y;
  }
  strokeWeight(4);
  lover_one_new_x = lover_one_previous_x + random(-100,100)/10 + rate*willingness;
  lover_one_new_y = lover_one_previous_y - random(-100,100)/10 - rate*1;
  lover_two_new_x = lover_two_previous_x - random(-100,100)/10 - rate*willingness;
  lover_two_new_y = lover_two_previous_y - random(-100,100)/10 - rate*1;
  lover_one_previous_x = lover_one_new_x;
  lover_one_previous_y = lover_one_new_y;
  lover_two_previous_x = lover_two_new_x;
  lover_two_previous_y = lover_two_new_y;
  //stroke(235, 20);  
  //line(lover_one_previous_x, lover_one_previous_y, lover_one_new_x, lover_one_new_y);
 
  /*
  arc(a, b, c, d, start, stop)
  Parameters  
  a  float: x-coordinate of the arc's ellipse
  b  float: y-coordinate of the arc's ellipse
  c  float: width of the arc's ellipse by default
  d  float: height of the arc's ellipse by default
  start  float: angle to start the arc, specified in radians
  stop  float: angle to stop the arc, specified in radians
  */

  //line(lover_one_previous_x, lover_one_previous_y, lover_one_new_x, lover_one_new_y);
  //curve(lover_one_previous_x, lover_one_previous_y, lover_one_previous_x + random(-200,200), lover_one_previous_y + random(-200,200), lover_one_previous_x + random(-200,200), lover_one_previous_y + random(-200,200), lover_one_new_x, lover_one_new_y);
  if (frameCount % pulse > 0 && frameCount % pulse < 8) {
    heart_size = pulse/2;
  }
  smooth();
  noStroke();
  //fill(139,0,0, 255);
  //beginShape();
  //vertex(width/2, height/2 + 50 + heart_size/2); 
  //bezierVertex(width/2 + 10 + heart_size, height - height/2 + 10 - heart_size/2, width/2 + 100 + heart_size/2, height/2 - 50 - heart_size/2, width/2, height/2 - heart_size/4); 
  //vertex(width/2, height/2 + 50 + heart_size/2); 
  //bezierVertex(width/2 - 10 - heart_size, height - height/2 + 10 - heart_size/2, width/2 - 100 - heart_size/2, height/2 - 50 - heart_size/2, width/2, height/2 - heart_size/4); 
  //endShape();
  //heart_size = 0;
  strokeWeight(2);
  for(int i = 0; i < starlets.size(); i++) {
    current_starlet = starlets.get(i);
    if (((current_starlet.location.x > lover_one_new_x - 10 && current_starlet.location.x < lover_one_new_x + 10) 
    && (current_starlet.location.y > lover_one_new_y - 10 && current_starlet.location.y < lover_one_new_y + 10))
    || ((current_starlet.location.x > lover_two_new_x - 10 && current_starlet.location.x < lover_two_new_x + 10) 
    && (current_starlet.location.y > lover_two_new_y - 10 && current_starlet.location.y < lover_two_new_y + 10))) {
      current_starlet.displace("x");
      current_starlet.displace("y");
    }
    current_starlet.jitter();
    stroke(255,random(255), random(20), random(20));
    fill(255,20,147, 20);
    if (diameter < 0) {
      diameter = random(60);
    }
    diameter -= 5;
    current_radians = 2*PI;
    arc(current_starlet.location.x, current_starlet.location.y, diameter, diameter, 0, current_radians);
  }
  //fill(250,10,10, 200);
  //chance = random(0,10);
  //if(chance > 8) {
  //  stroke(255,20,20, 100);
  //}
  fill(255, 200);
  ellipse(lover_one_new_x, lover_one_new_y, 15, 15);
  //fill(65,105,225, 200);
  //if(chance > 8) {
  //  stroke(20,20,255, 100);
  //}
  fill(255, 200);
  ellipse(lover_two_new_x, lover_two_new_y, 15, 15);
  noStroke();
  translate(width/2, height/2);
  for(int x = -110; x <= 110; x+=10){
    for(int y = -110; y <= 110; y+=10){
      float d = dist(x, y, 0, 0);
      float d2 = sin(radians(d))*d;
      fill(255, 230, 230);
      pushMatrix();
      translate(x, y);
      rotate(radians(d + frameCount));
      int num = 1;
      if(random(1,100) < 90) {
        num = -1;
      }
      ellipse(x, num * y, 5, 5);
      popMatrix();
    } 
  }
  count++;
}

void fade(int trans)
{
  noStroke();
  fill(100,trans);
  rect(0,0,width,height);
}

class Starlet {
  PVector location;

  Starlet(PVector location) {
    this.location = location;
  }

  void jitter() {
    //stroke(0, 150, 255, map(life, 0, maxLife, 1, 255));
    stroke(212,175,55);
    point(location.x + random(-2, 2), location.y + random(-2, 2));
  }
  
  void displace(String coordinate) {
    //if (coordinate == "x") {
      location.x += random(100,-100);
    //} else {
      location.y += random(100,-100);
    //}
  }
}