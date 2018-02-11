#include <string>
#include <iostream>
#include <sstream>
#include <stdlib.h>
#include "SFML/include/SFML/Graphics.hpp"
#include <math.h>
#include <pthread.h>
#include <thread>
#include <future>
#define Pi 3.14159265

using namespace sf;
using namespace std;
int rr(int min,int max){
  int ret = min + (rand() % (int)(max - min + 1));
  return ret;
}
bool dist3d(float p1[3], float p2[3]){
  return sqrt(pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)+ pow((p1[2] - p2[2]), 2)) < p2[3];
}

float dist3sphere(float x,float y,float z,float x2,float y2,float z2){
  float distance;
  distance = sqrt(pow((x - x2), 2) + pow((y - y2), 2) + pow((z - z2), 2));
  return(distance);
}

float dist3p(float a[3], float b[4]){
  return dist3sphere(a[0],a[1],a[2],b[0],b[1],b[2]) < b[3];
}
float *rayang(float direc[3]){
  return direc;
}

Color getPixel(int x,int y, int size[2], float objs[][4]){
    float raySpread = 0.05;
    float raypos[3] = {0,0,0};
    float raydir[3] = {0,(x-size[0]/2)*raySpread,(y-size[1]/2)*raySpread};

    float crx = raydir[2] * Pi / 180.0;
    float cry = raydir[0] * Pi / 180.0;
    float crz = raydir[1] * Pi / 180.0;
    raydir[2] = sin(crz);
    raydir[1] = -(sin(crx) * cos(crz));
    raydir[0] = cos(crx) * cos(cry);

    for (int rayits = 0; rayits < 25; rayits ++){
      for (int objc = 0; objc < 15; objc ++){
        if (dist3p(raypos,objs[objc])){
          //cout << dist3d(raypos,objs[objc]) << endl;
          return Color(255,255,raypos[0]*10,255);
        }
      }
      for (int coord = 0; coord < 3; coord ++){
        raypos[coord] += raydir[coord];
      }
    }
    return Color(0,0,0,0);
}
int main(){
  int size[2] = {2000,2000};
  RenderWindow window(VideoMode(size[0],size[1]),"render");
  float objs[50][4];
  for (int i = 0; i < 15; i++){
    objs[i][0] = 15;
    objs[i][1] = sin(i)*15;
    objs[i][2] = cos(i)*15;
    objs[i][3] = 3;
  }
  Event e;
  Image image;
  image.create(size[0], size[1], Color(100,100,100,255));
  window.clear();
  int FrameCount = 0;
  while (window.isOpen()){
    while (window.pollEvent(e)){
      if (e.type == Event::Closed){
        window.close();
      }
    }
    window.clear();
    int blk = 2;
    for (int xp = 0; xp < size[0]; xp += blk){
      for (int yp = 0; yp < size[1]; yp += blk ){
        Color c = getPixel(xp,yp,size,objs);
        for (int x = 0; x < blk; x++){
          for (int y = 0; y < blk; y++){
            image.setPixel(xp+x,yp+y,c);
          }
        }
      }
      Sprite sprite;
      Texture texture;
      texture.loadFromImage(image);
      sprite.setTexture(texture);
      window.clear();
      window.draw(sprite);
      window.display();
    }
    window.close();
    image.saveToFile("scrot/grab.png");
  }
  return 0;
}
