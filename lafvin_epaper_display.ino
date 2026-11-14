#include <SPI.h>
#include <math.h>
#include "epd2in13_V4.h"
#include "epdpaint.h"
#include "star.h"
#include "messages.h"

#define COLORED     0
#define UNCOLORED   1

/**
  * Due to RAM not enough in Arduino UNO, a frame buffer is not allowed.
  * In this case, a smaller image buffer is allocated and you have to 
  * update a partial display several times.
  * 1 byte = 8 pixels, therefore you have to set 8*N pixels at a time.
  */
unsigned char image[1050];
Epd epd; // ePaper display driver
int button_pin = 3; // Arduino pin connected to button

// Artist - used to draw to the image buffer
// Width should be a multiple of 8
Paint paint(image, epd.bufwidth*8, epd.bufheight, ROTATE_90);


void setup()
{
  pinMode(button_pin, INPUT);
  Serial.begin(115200);
  epd.Init(FAST);
  epd.Init(FULL);
  // epd.Display_Fast(star);
  // epd.Display1(star);
  delay(100);

  // epd.Init(FULL);

  helloWorld(paint, epd, image);

  delay(100);
  // epd.Init(FULL);
  // epd.Clear(UNCOLORED);
  // epd.Sleep();

}

void loop()
{
  int button_state = digitalRead(button_pin);
  if (button_state == HIGH) {
    paint.Clear(UNCOLORED);
    paint.DrawStringAt(1, 15, "Hi Eleano", &Font12, COLORED);
    epd.Display1(image);

    paint.Clear(UNCOLORED);
    paint.DrawStringAt(1, 15, "r!", &Font12, COLORED);
    epd.Display1(image);

    paint.Clear(UNCOLORED);
    // paint.DrawStringAt(1, 15, "jaliburn", &Font12, COLORED);
    epd.Display1(image);

    paint.Clear(UNCOLORED);
    // paint.DrawStringAt(1, 15, "dornt", &Font12, COLORED);
    epd.Display1(image);
  }
  // epd.Sleep();
  delay(100);
}