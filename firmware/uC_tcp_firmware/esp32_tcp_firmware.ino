// ESP32 WiFi TCP Firmware v0.2b for Serial communication w/ audio-visualiser
// Audio Visualiser by Frank Fourlas is licensed under CC BY-NC-SA 4.0.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0
// This firmware file is included in the license above

#include <WiFi.h>
#include <FastLED.h>

#define NUM_LEDS 40
#define LED_TYPE NEOPIXEL
#define PIN 16

const char ssid[] = "SSID";
const char pass[] = "PASS";
const int port = 25566;

CRGB leds[NUM_LEDS];

WiFiServer server(port);

void setup() {
  while(!Serial.begin(115200));
  
  FastLED.addLeds<LED_TYPE, PIN>(leds, NUM_LEDS);
  clear();
  
  Serial.print("Attempting to connect to WiFi network ");
  Serial.println(ssid);
  WiFi.disconnect(true);
  while(!WiFi.begin(ssid, pass));
  delay(3000);
  Serial.print("Connected! IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
  server.setNoDelay(true);
}

void loop() {
  long t;
  byte tt;
  WiFiClient client = server.available();
  
  if(client){
    
    // Handshake
    Serial.print("New connection request from ");
    Serial.println(client.remoteIP());
    client.print(client.remoteIP().toString() + " ACK");
    client.flush();

    while (true){
      t = millis();
      // Wait for new frame
      WAIT:while(client.available() < 1)  // 0xFF is new frame ack packet
      if(client.read() != 0xFF) goto WAIT;
      // Get pixel data
      NEWFRAME:while(client.available() < 3*NUM_LEDS);
      for (int i = 0; i < NUM_LEDS; i++) {
        leds[i].r = client.read();
        if (leds[i].r == 0xFF) goto NEWFRAME;
        leds[i].g = client.read();
        if (leds[i].g == 0xFF) goto NEWFRAME;
        leds[i].b = client.read();
        if (leds[i].b == 0xFF) goto NEWFRAME;
//        Serial.print(leds[i].r);
//        Serial.print(".") ;
//        Serial.print(leds[i].g);
//        Serial.print(".") ;
//        Serial.print(leds[i].b);
//        Serial.print(" ");
      }
//      Serial.print("\n");
      FastLED.show();
      delay(25);
//      Serial.print("FPS: ");
//      Serial.println(1000 / (millis() - t));
    }

    client.stop();
    Serial.println("\nClient Disconnected");
  }
}

void clear(){
  memset(leds, 0, NUM_LEDS*3);
  FastLED.show();
}
