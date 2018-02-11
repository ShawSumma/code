#include "head.hpp"
int main(){
  #include "colors.hpp"
  int size[2];
  size[0] = 1200;
  size[1] = 1200;
  RenderWindow window(VideoMode(size[0],size[1]),"render");
  int pixelsize = 6;
  float raySpread = 0.002;
  float maxrays[2];
  maxrays[0] = size[0]/2*raySpread;
  maxrays[1] = size[1]/2*raySpread;

  float player;

  float sphere[4];
  sphere[0] = 40;
  sphere[1] = 0;
  sphere[2] = 0;
  sphere[3] = 50;

  float cube[6];
  cube[0] = 0;
  cube[1] = 0;
  cube[2] = 5;
  cube[3] = 50;
  cube[4] = 50;
  cube[5] = 5;

  for (int i = 0; i < 6; i++){
    cout << cube[i] << ' ';
  }
  cout << endl;
  for (int i = 0; i < 3; i++){
    cout << sphere[i] << ' ';
  }
  cout << endl;
  cout << endl;
  float lps = Pi/2;
  while (window.isOpen()){
    //player[2] -= .5;
    //cube[2] += .1;
    Image image;
    Event e;
    while (window.pollEvent(e)){
      if (e.type == Event::Closed){
        window.close();
      }
    }
    image.create(size[0], size[1], greyPixel);
    for (int x = 0; x < size[0]; x += pixelsize){
      for (int y = 0; y < size[1]; y +=  pixelsize){
        float raypos[3];
        for (int i = 0; i < 3; i++){
          //raypos[i] = player[i];
        }
        float raydir[3];
        raydir[0] = 1;
        raydir[1] = (x-size[0]/2)*raySpread;
        raydir[2] = (y-size[1]/2)*raySpread;
        for (int iters = 0; iters < 100; iters++){
          if (dist3bool(raypos,sphere)){
            for (int xp = 0; xp < pixelsize; xp++){
              for (int yp = 0; yp < pixelsize; yp++){
                ///cout << x+xp << " " << x+yp << endl;
                image.setPixel(x+xp,y+yp,redPixel);
              }
            }
            break;
          }
          if (distCbool(raypos,cube)){
            for (int xp = 0; xp < pixelsize; xp++){
              for (int yp = 0; yp < pixelsize; yp++){
                ///cout << x+xp << " " << x+yp << endl;
                image.setPixel(x+xp,y+yp,whitePixel);
              }
            }
            break;
          }
          for (int axis = 0; axis < 3; axis++){
            raypos[axis] += raydir[axis];
          }
        }
        cout << raydir[0] << ' ' << raydir[1] << endl;
      }
    }
    cout << "Frame" << endl;
    window.clear();
    Sprite sprite;
    Texture texture;
    texture.loadFromImage(image);
    sprite.setTexture(texture);
    window.clear();
    window.draw(sprite);
    window.display();
    //lps += 0.1;
  }
}
