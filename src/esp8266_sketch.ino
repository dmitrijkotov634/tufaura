#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

const uint8_t R_LED = 4;
const uint8_t G_LED = 0;
const uint8_t B_LED = 2;

WiFiServer wifiServer(55663);
WiFiClient client;

boolean freeze = false;
long lastRequest = 0;

void setRGB(uint8_t r, uint8_t g, uint8_t b) {
    analogWrite(R_LED, 1023 - map(r, 0, 255, 0, 1023));
    analogWrite(G_LED, 1023 - map(g, 0, 255, 0, 1023));
    analogWrite(B_LED, 1023 - map(b, 0, 255, 0, 1023));
}

void setup() {
  pinMode(R_LED, OUTPUT);
  pinMode(G_LED, OUTPUT);
  pinMode(B_LED, OUTPUT);

  analogWriteRange(1023);

  setRGB(0, 0, 0);

  Serial.begin(9600);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.println(WiFi.localIP());

  wifiServer.begin();
}

void handleClient() {
  if (!client || !client.connected()) {
    client = wifiServer.available();
    if (client) {
      Serial.println("Client connected!");
    } else {
      if (!freeze) {
        setRGB(0, 0, 0);
      }
      lastRequest = millis();
      return;
    }
  }

  if (client.connected()) {
    while (client.available() > 0) {
      char command = client.read();
      switch (command) {
        case 's':
          {
            String colorStr = client.readStringUntil(';');
            int color = colorStr.toInt();
            uint8_t r = (color >> 16) & 0xFF;
            uint8_t g = (color >> 8) & 0xFF;
            uint8_t b = color & 0xFF;
            setRGB(r, g, b);
            break;
          }
        case 'f':
          {
            freeze = true;
            Serial.println("Freeze mode enabled.");
            break;
          }
        case 'r':
          {
            freeze = false;
            Serial.println("Freeze mode disabled.");
            break;
          }
        default:
          {
            Serial.print("Unknown command: ");
            Serial.println(command);
            break;
          }
      }

      client.print(".");
      lastRequest = millis();
    }

    if (millis() - lastRequest > 3000) {
      Serial.println("Client timeout. Disconnecting...");
      client.stop();
    }
  }
}

void loop() {
  handleClient();
}
