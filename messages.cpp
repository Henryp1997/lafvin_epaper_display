#include "epd2in13_V4.h"
#include "epdpaint.h"
#include "messages.h"

#define COLORED     0
#define UNCOLORED   1

void helloWorld(Paint& paint, Epd& epd, unsigned char* image) {
  paint.Clear(UNCOLORED);
  paint.DrawStringAt(1, 10, "Hello, wo", &Font12, COLORED);
  epd.Display1(image);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(1, 10, "rld!", &Font12, COLORED);
  // paint.DrawStringAt(29, 10, "b", &Font12, COLORED);
  paint.DrawStringAt(1, 115, "        P", &Font12, COLORED);
  epd.Display1(image);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(1, 115, "ress the ", &Font12, COLORED);
  epd.Display1(image);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(1, 115, "button...", &Font12, COLORED);
  epd.Display1(image);
}

// void allSameChar(Paint& paint, Epd& epd, unsigned char* image) {
//   paint.Clear(UNCOLORED);
//   paint.DrawStringAt(7, 12, "lllllllll", &Font12, COLORED);
//   epd.Display1(image);

//   paint.Clear(UNCOLORED);
//   paint.DrawStringAt(0, 12, "lllllllll", &Font12, COLORED);
//   epd.Display1(image);

//   paint.Clear(UNCOLORED);
//   paint.DrawStringAt(1, 12, "lllllllll", &Font12, COLORED);
//   epd.Display1(image);

//   paint.Clear(UNCOLORED);
//   paint.DrawStringAt(1, 12, "llllllll", &Font12, COLORED);
//   epd.Display1(image);
// }
