#include <WiFi.h>

const char* ssid = "RBA-LT.2";
const char *password = "RBA2025$";

void setup() {
  // This is for the connection through WIFI 
  Serial.begin(115200);
  delay(1000);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.println(WiFi.localIP());
}

void loop() {
  String input = "";

  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
  }
}
