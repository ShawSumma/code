//if g++ main.cpp -lsfml-graphics  -lsfml-window -lsfml-system; then ./a.out; fi
#include "SFML/include/SFML/Graphics.hpp"
#include <time.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

using namespace sf;
using namespace std;

bool distCbool(float pos[3], float cube[6]){
  float a = abs(pos[0]-cube[0]);
  float b = abs(pos[1]-cube[1]);
  float c = abs(pos[2]-cube[2]);
  if (a < cube[3] && b < cube[4] && c < cube[5]){
    return true;
  }
  return false;
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
#define Pi 3.14159265
