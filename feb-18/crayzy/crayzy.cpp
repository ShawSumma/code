//if g++ main.cpp -lsfml-graphics  -lsfml-window -lsfml-system; then ./a.out; fi
#include "SFML/include/SFML/Graphics.hpp"
#include <time.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include "distfns.hpp"

using namespace sf;
using namespace std;

Sprite imgToSpr(Image image){
  Sprite sprite;
  Texture texture;
  texture.loadFromImage(image);
  sprite.setTexture(texture);
  return sprite;
}
bool doesHit(int raydata[2][3], int hitbox[2][3]){
  if (hitbox[0][0] < raydata[0][0] && raydata[0][0] < hitbox[1][0]){
    if (hitbox[0][1] < raydata[0][1] && raydata[0][1] < hitbox[1][1]){
      if (hitbox[0][2] < raydata[0][2] && raydata[0][2] < hitbox[1][2]){
        return true;
      }
    }
  }
  return false;
}
bool hits(){
  
}
bool normBox(int hitbox[2]){;
    if (hitbox[0] > hitbox[1]){
      return true;
    }
    return false;
}
int main(){
    int size[2];
    size[0] = 400;
    size[1] = 400;
    RenderWindow window(VideoMode(size[0],size[1]),"edit");

    Color blackPixel(0,0,0,255);
    Color whitePixel(255, 255, 255, 255);
    Color greyPixel(127,127,127, 255);
    int worldBox[2][2][3];
    for (int obj = 0; obj < 2; obj ++){
      if (obj == 0){
        worldBox[obj][0] = 40;
        worldBox[obj][1] = 20;
        worldBox[obj][2] = 20;
        worldBox[obj][3] = 2;
      }
    }
    /*
    for (int obj = 0; obj < 2; obj ++){
      for (int x = 0; x < 3; x++){
        //cout << "is "<< normBox(worldBox[x]) << endl;
        if (worldBox[obj][0][x] > worldBox[obj][1][x]){

          float hold = worldBox[obj][0][x];
          worldBox[obj][0][x] = worldBox[obj][1][x];
          worldBox[obj][1][x] = hold;
        }
      }
    }
    */
    cout << '\n';
    int loops = 0;
    while (window.isOpen()){
      Image image;
      image.create(size[0], size[1], blackPixel);
      Event e;
      while (window.pollEvent(e)){
        if (e.type == Event::Closed){
          window.close();
        }
      }
      Vector2i position = sf::Mouse::getPosition(window);
      int mousepos[2];
      mousepos[0] = position.x-size[0]/2;
      mousepos[1] = position.y-size[0]/2;
      worldBox[0][0][1] = mousepos[0] - 50;
      worldBox[0][0][2] = mousepos[1] - 50;
      worldBox[0][1][1] = mousepos[0] + 50;
      worldBox[0][1][2] = mousepos[1] + 50;
      for (int x = 0; x < size[0]; x++){
        for (int y = 0; y < size[1]; y++){
          image.setPixel(x,y,blackPixel);
          int raydata[2][3];
          raydata[0][0] = 0;
          raydata[0][1] = x-size[0]/2;
          raydata[0][2] = y-size[1]/2;
          raydata[1][0] = -1;
          raydata[1][1] = (y-size[0]/2)*0.02;
          raydata[1][1] = (x-size[0]/2)*0.02;
          for (int its = 0; its < 50; its++){
              for (int i = 0; i < 3; i++){
                raydata[0][i] += raydata[1][i];
              }
              for (int obj = 0; obj < 2; obj++){
                bool runit = doesHit(raydata,worldBox[obj]);
                if (runit){
                  image.setPixel(x,y,greyPixel);
                  break;
                }
              }
            }
          //cout << raydata[0][1] << endl;
        }
      }

      cout << "done\n";
      Sprite sprite;
      Texture texture;
      texture.loadFromImage(image);
      sprite.setTexture(texture);
      window.draw(sprite);
      window.display();
      loops ++;
    }
}
