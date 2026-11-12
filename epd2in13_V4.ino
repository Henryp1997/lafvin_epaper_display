#include <SPI.h>
#include <math.h>
#include "epd2in13_V4.h"
#include "epdpaint.h"
#include "star.h"

#define COLORED     0
#define UNCOLORED   1

/**
  * Due to RAM not enough in Arduino UNO, a frame buffer is not allowed.
  * In this case, a smaller image buffer is allocated and you have to 
  * update a partial display several times.
  * 1 byte = 8 pixels, therefore you have to set 8*N pixels at a time.
  */
unsigned char image[1050];
Paint paint(image, 0, 0, 0);
Epd epd;

void setup()
{
  Serial.begin(115200);
  Serial.println("epd FAST");
  epd.Init(FAST);
  // epd.Init(FULL);
  epd.Display_Fast(star);
  // epd.Display1(star);
  delay(100);

  Serial.println("epd FULL");
  epd.Init(FULL);
  Paint paint(image, epd.bufwidth*8, epd.bufheight, ROTATE_0); // width should be the multiple of 8

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(20, 15, "Smart Display", &Font12, COLORED);
  paint.DrawRectangle(5, 5, 115, 35, COLORED);
  epd.Display1(image);
  // delay(100);
  
  // paint.Clear(UNCOLORED);
  paint.DrawStringAt(10, 25, "Weather:", &Font12, COLORED);
  paint.DrawStringAt(10, 45, "Sun 26C", &Font12, COLORED);
  epd.Display1(image);
  // delay(100);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(15, 5, "System Init...", &Font12, COLORED);
  paint.DrawRectangle(10, 25, 110, 35, COLORED);
  for(int i = 0; i < 100; i += 20) {
    paint.DrawFilledRectangle(11, 26, 11 + i, 34, COLORED);
    epd.Display1(image);
    delay(100);
  }
  
  paint.Clear(UNCOLORED);
  paint.DrawStringAt(20, 15, "Ready to use", &Font12, COLORED);
  epd.Display1(image);

  delay(100);
  epd.Init(FULL);
  Serial.println("e-Paper clear and sleep");
  // epd.Clear(UNCOLORED);
  epd.Sleep();

}

void loop()
{

}