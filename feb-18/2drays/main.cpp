#include "SFML/include/SFML/Graphics.hpp"
#include <stdlib.h>
#include <iostream>
#include <math.h>
using namespace sf;
using namespace std;
#define Pi 3.14159265
float* eu2vel(float raydir[3]){
  float crx = raydir[2] * Pi / 180.0;
  float cry = raydir[0] * Pi / 180.0;
  float crz = raydir[1] * Pi / 180.0;
  raydir[2] = sin(crz);
  raydir[1] = -(sin(crx) * cos(crz));
  raydir[0] = cos(crx) * cos(cry);
  return (float*) raydir;
}
bool dist3c(float x,float y,float z,float x2,float y2,float z2, float dist){
  if (x > x2 + dist) return 0;
  if (x < x2 - dist) return 0;
  if (y > y2 + dist) return 0;
  if (y < y2 - dist) return 0;
  if (z > z2 + dist) return 0;
  if (z < z2 - dist) return 0;
  return 1;
}
bool dist3s(float x,float y,float z,float x2,float y2,float z2, float dist){
  float distance;
  distance = sqrt(pow((x - x2), 2) + pow((y - y2), 2) + pow((z - z2), 2));
  return(distance < dist);
}
int main(){
  float box[10][4] = {{0,0,10,1}};

  int size[2] = {160,90};
  RenderWindow window(VideoMode(size[0],size[1]),"render");
  Event e;
  Image image;
  int blk = 1;
  float raySpread = 0.5;
  float loops = 0;
  float xang;
  float yang;
  float ppos[3] = {0,0,0};
  while (window.isOpen()){
    image.create(size[0], size[1], Color(100,100,100,255));
    if (Keyboard::isKeyPressed(Keyboard::W)){
      ppos[0] += 0.2;
    }
    if (Keyboard::isKeyPressed(Keyboard::S)){
      ppos[0] -= 0.2;
    }
    while (window.pollEvent(e)){
      if (e.type == Event::Closed){
        window.close();
      }
    }
    Vector2i mpos = sf::Mouse::getPosition(window);
    for (int xp = 0; xp < size[0]; xp += blk){
      for (int yp = 0; yp < size[1]; yp += blk ){
        xang = (xp-size[0]/2)*raySpread+mpos.x;
        yang = (yp-size[1]/2)*raySpread+mpos.y;
        float rayeul[3] =  {0,xang,yang};
        float* raydir = eu2vel(rayeul);
        double rgb[3] = {255,255,255};
        float raypos[3];
        for (int ax = 0; ax < 3; ax++){
          raypos[ax] = ppos[ax];
        }
        for (int len = 0; len < 250; len++){
          for (int ax = 0; ax < 3; ax++){
            raypos[ax] += raydir[ax];
          }
          for (int i = 0; i < 10; i++){
            if (dist3c(raypos[0],raypos[1],raypos[2],box[i][0],box[i][1],box[i][2],box[i][3])){
              for (int r = 0; i < 3; i++){
                rgb[i] = 0;
              }
              len = 5000;
              break;
            }
          }
        }

        //cout << raydir[0] << endl;
        Color setcol(rgb[0],rgb[1],rgb[2],255);
        image.setPixel(xp,yp,setcol);
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
    loops ++;
  }
}
