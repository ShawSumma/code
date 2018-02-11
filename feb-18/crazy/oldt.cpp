//g++ main.cpp -lsfml-graphics  -lsfml-window -lsfml-system
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
float dist3cube(float x,float y,float z,float x2,float y2,float z2){
  float out;
  out = dist(x,y,x2,y2);
  return(out);
}
float in3cube(float x,float y,float z,float x2,float y2,float z2, float size){
  bool out;
  bool xis = x2 - size < x < x2 + size;
  bool zis = y2 - size < y < y2 + size;
  bool yis = z2 - size < z < z2 + size;
  out = xis && yis && zis;
  //cout << x << " " << y << " " << z << " " << x2 << " " << y2 << " " << z2 << " " << endl;
  return(out);
}
int main(){
  int size[2];
  size[0] = 1200;
  size[1] = 1200;
  cout << in3cube(0,0,0,1,1,1,2) << endl;
  RenderWindow window(VideoMode(size[0],size[1]),"render");
  Color blackPixel(0,0,0,255);
  Color whitePixel(255, 255, 255, 255);
  int block = 5;
  while (window.isOpen()){
    Image image;
    image.create(size[0], size[1], blackPixel);

    Vector2i position = sf::Mouse::getPosition(window);
    int mousepos[2];
    mousepos[0] = position.x-600;
    mousepos[1] = position.y-600;
    float toff;
    for (int xp = 0; xp < size[0]; xp += block){
      for (int yp = 0; yp < size[1]; yp += block){
        float raypos[3];
        float raymov[3];
        raypos[0] = 0;
        raypos[1] = 0;
        raypos[2] = 0;
        raymov[0] = 1.5;
        raymov[1] = (xp-size[0]/2)*0.02;
        raymov[2] = (yp-size[1]/2)*0.02;
        toff = dist3sphere(0,0,0,raymov[0],raymov[1],raymov[2]);
        for (int leng = 0; leng < 500; leng+= toff){
          raypos[0] += raymov[0];
          raypos[1] += raymov[1];
          raypos[2] += raymov[2];
          if (raypos[2] > 10){
            Color nowPixel(100,100,100,255);
            for (int xa = 0; xa < block; xa++){
              for (int ya = 0; ya < block; ya++){
                image.setPixel(xp+xa,yp+ya,nowPixel);
              }
            }
            break;
          }
          float adist = in3cube(raypos[0],raypos[1],raypos[2],20,0,0,0.5);
          if (adist){
            //cout << adist << endl << raypos[0] << endl << endl;
            Color nowPixel(255,255,255,255);
            for (int xa = 0; xa < block; xa++){
              for (int ya = 0; ya < block; ya++){
                image.setPixel(xp+xa,yp+ya,nowPixel);
              }
            }
            break;
          }
          if (yp > size[1]){
            break;
          }
        }
        //cout << raypos[0] << endl << raypos[1] << endl << endl;
      }
    }
    cout << "frame" << endl;
    Sprite sprite;
    Texture texture;
    texture.loadFromImage(image);
    sprite.setTexture(texture);
    window.clear();
    window.draw(sprite);
    window.display();
  }
}
