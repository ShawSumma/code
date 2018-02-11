#include <iostream>
#include "SFML/include/SFML/Graphics.hpp"
using namespace std;
int main(){
  RenderWindow window(VideoMode(size[0],size[1]),"render");
  while (window.isOpen()){
    Image image;
    Event e;
    while (window.pollEvent(e)){
      if (e.type == Event::Closed){
        window.close();
      }
    }
  }
}
