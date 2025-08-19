#include <WiFi.h>

#define BUZZER 32
#define SERVO_PIN 13
#define TRIG_PIN 26
#define ECHO_PIN 27

WiFiServer server(80);
WiFiClient client;
String request;

const char* ssid = "RBA-LT.2";
const char* password = "RBA2025$";

void setup() {
  // put your setup code here, to run once:
  pinMode(BUZZER, OUTPUT);
  Serial.begin(9600);

  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");
  while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  digitalWrite(BUZZER, LOW);
  delay(200);
  digitalWrite(BUZZER, HIGH);
  delay(200);
  digitalWrite(BUZZER, LOW);
  delay(200);

  Serial.print("http://");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

  // listen to every client
  client = server.available();
  if (!client) {
    return;
  }

  while (client.connected()) {
    if (client.available()) {
      String message = client.readStringUntil('\n'); 

      message.trim();

      Serial.print(message);
      if (request.indexOf("GET /test")){
        digitalWrite(BUZZER, LOW);
        delay(200);
        digitalWrite(BUZZER, HIGH);
        delay(200);
        digitalWrite(BUZZER, LOW);
        delay(200);
      }

      
    }

  delay(1);
  client.stop();
  }

}
