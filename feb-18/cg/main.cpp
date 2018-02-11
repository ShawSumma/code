//if g++ main.cpp -lsfml-graphics  -lsfml-window -lsfml-system; then ./a.out; fi
#include "SFML/include/SFML/Graphics.hpp"
#include <time.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#define Pi 3.14159265

using namespace sf;
using namespace std;


int rr(int min,int max){
  int ret = min + (rand() % (int)(max - min + 1));
  return ret;
}
float dist(double x1, double y1, double x2, double y2){
  double square_difference_x = (x2 - x1) * (x2 - x1);
  double square_difference_y = (y2 - y1) * (y2 - y1);
  double sum = square_difference_x + square_difference_y;
  double value = sqrt(sum);
  return value;
}
float dist3sphere(float x,float y,float z,float x2,float y2,float z2){
  float distance;
  distance = sqrt(pow((x - x2), 2) + pow((y - y2), 2) + pow((z - z2), 2));
  return(distance);
}

float dist3p2(float a[3], float b[3]){
  return dist3sphere(a[0],a[1],a[2],b[0],b[1],b[2]);
}
float dist3ig(float a[3], float b[4]){
  return dist3sphere(a[0],a[1],a[2],b[0],b[1],b[2]);
}
bool dist3bool(float a[3], float b[4]){
  return dist3p2(a,b) < b[3];
}
bool dist3bo(float a[3], float b[4]);
Color colorize(int objcount, int sphere[6][4], float raydir[3]){
  float raypos[3];
  for (int i = 0; i < 3; i++){
    raypos[i] = 0;
  }

  //cout << raydir[0] << endl << raydir[1] << endl << raydir[2] << endl << endl;
  float crx = raydir[2] * Pi / 180.0;
  float cry = raydir[0] * Pi / 180.0;
  float crz = raydir[1] * Pi / 180.0;
  //cout << crx << endl << cry << endl << crz << endl << endl;

  raydir[2] = sin(crz);
  raydir[1] = -(sin(crx) * cos(crz));
  raydir[0] = cos(crx) * cos(cry);
  //cout << raydir[0] << endl << raydir[1] << endl << raydir[2] << endl << endl << endl << endl;

  for (int iters = 0; iters < 100; iters++){
    for (int s = 0; s < objcount; s++){
      if (dist3bool(raypos,sphere[s])){
        return Color(255,255,255,255);
      }
    }
    for (int axis = 0; axis < 3; axis++){
      raypos[axis] += raydir[axis];
    }
  }
  return Color(0,0,0,255);
}
int main(){
  int size[2];
  size[0] = 600;
  size[1] = 600;
  RenderWindow window(VideoMode(size[0],size[1]),"render");
  int pixelsize = 1;
  float raySpread = 0.1;
  float maxrays[2];
  maxrays[0] = size[0]/2*raySpread;
  maxrays[1] = size[1]/2*raySpread;

  float player;
  int objcount = 6;
  float sphere[objcount][4];
  sphere[0][0] = 15;
  sphere[0][1] = 0;
  sphere[0][2] = 0;
  sphere[0][3] = 3;
  sphere[1][0] = -15;
  sphere[1][1] = 0;
  sphere[1][2] = 0;
  sphere[1][3] = 3;
  sphere[2][0] = 0;
  sphere[2][1] = 0;
  sphere[2][2] = 15;
  sphere[2][3] = 3;
  sphere[3][0] = 0;
  sphere[3][1] = 0;
  sphere[3][2] = -15;
  sphere[3][3] = 3;
  sphere[4][0] = 0;
  sphere[4][1] = 15;
  sphere[4][2] = 0;
  sphere[4][3] = 3;
  sphere[5][0] = 0;
  sphere[5][1] = -15;
  sphere[5][2] = 0;
  sphere[5][3] = 3;
  float lps = 0;
  while (window.isOpen()){
    float max = 100;
    Vector2i position = Mouse::getPosition(window);
    //player[2] -= .5;
    //cube[2] += .1;
    Event e;
    while (window.pollEvent(e)){
      if (e.type == Event::Closed){
        window.close();
      }
    }
    Image image;
    image.create(size[0], size[1], Color(100,100,100,255));

    Color colors[size[0]][size[1]];
    float raydir[3];
    for (int x = 0; x < size[0]; x += pixelsize){
      for (int y = 0; y < size[1]; y +=  pixelsize){
        raydir[0] = 1;
        raydir[1] = (x-size[0]/2)*raySpread;
        raydir[2] = (y-size[1]/2)*raySpread;
        colors[x][y] = Color(255,255,255);
      }
    }
    //cout << raydir[1] << endl;
    //cout << "Frame" << endl;
    window.clear();
    Sprite sprite;
    Texture texture;
    texture.loadFromImage(image);
    sprite.setTexture(texture);
    window.clear();
    window.draw(sprite);
    window.display();
    lps += 0.1;
  }
}
