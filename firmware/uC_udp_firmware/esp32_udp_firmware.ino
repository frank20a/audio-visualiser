// ESP32 WiFi UDP Firmware v0.1a for Serial communication w/ audio-visualiser
// Audio Visualiser by Frank Fourlas is licensed under CC BY-NC-SA 4.0.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0
// This firmware file is included in the license above

#include <WiFi.h>
#include <WiFiUdp.h>
#include <FastLED.h>

#define NUM_LEDS 66
#define LED_TYPE NEOPIXEL
#define PIN 16

const char ssid[] = "SSID";
const char pass[] = "PASS";
const int port = 25566;

CRGB leds[NUM_LEDS];

WiFiUDP server;

void setup() {
  Serial.begin(115200);
  
  FastLED.addLeds<LED_TYPE, PIN>(leds, NUM_LEDS);
  clear();
  
  Serial.print("Attempting to connect to WiFi network ");
  Serial.println(ssid);
  WiFi.disconnect(true);
  while(!WiFi.begin(ssid, pass));
  delay(3000);
  Serial.print("Connected! IP: ");
  Serial.println(WiFi.localIP());

  while(!server.begin(port));
  
}

void loop() {
//  long t = millis();
  while(!server.parsePacket());
  server.read((byte *)leds, 3*NUM_LEDS);
  FastLED.show();
//  Serial.print("FPS: ");
//  Serial.println(1000 / (millis() - t));
}

void clear(){
  memset(leds, 0, NUM_LEDS*3);
  FastLED.show();
}
