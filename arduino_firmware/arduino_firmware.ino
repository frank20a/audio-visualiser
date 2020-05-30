#include <FastLED.h>

#define NUM_LEDS 60
#define LED_TYPE NEOPIXEL
#define PIN 6

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, PIN>(leds, NUM_LEDS);
  
  Serial.begin(250000);
  pinMode(12, OUTPUT);
  Serial.println("Arduino say HELLO");
}

void loop() {
  get_vals();
  FastLED.show();
}

void get_vals(){
  for (int i = 0; i < NUM_LEDS; i++){
    while (Serial.available() < 3);
    unsigned char temp[3];
    Serial.readBytes(temp, 3);
    leds[i].r = temp[0];
    leds[i].g = temp[1];
    leds[i].b = temp[2];
  }
  Serial.write('#');
}

//void clear(){
//  memset(leds, 0, NUM_LEDS*3);
//}
