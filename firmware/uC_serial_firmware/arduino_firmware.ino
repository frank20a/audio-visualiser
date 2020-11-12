// Arduino Firmware v0.3.1 for Serial communication w/ audio-visualiser
// Audio Visualiser by Frank Fourlas is licensed under CC BY-NC-SA 4.0.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0
// This firmware file is included in the license above

#include <FastLED.h>

#define NUM_LEDS 40
#define LED_TYPE NEOPIXEL
#define PIN 16

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, PIN>(leds, NUM_LEDS);
  clear();
  
  Serial.begin(500000);

  // Handshake
  Serial.println("Hello World");
}

void loop() {
  get_vals();
  FastLED.show();
}

void get_vals(){

  // Wait for new-frame byte
  while (Serial.available() < 1);
  if (Serial.read() == 0xFF){
    
//    byte temp[3];
    for (int i = 0; i < NUM_LEDS; i++){
      //while (Serial.available() < 3);
      Serial.readBytes((byte*)(&leds[i]), 3);
    }
    
  }
//  Serial.write('#');
}

void clear(){
  memset(leds, 0, NUM_LEDS*3);
  FastLED.show();
}
