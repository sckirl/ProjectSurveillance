#define LAMP 32
#define SERVO_PIN 13
#define TRIG_PIN 26
#define ECHO_PIN 27

#include "BluetoothSerial.h"
#include <ESP32Servo.h>
#include <WiFi.h>

BluetoothSerial SerialBT;
Servo servo;
float duration, distance;

void setup() {
  // attach everything
  pinMode(LAMP,OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  servo.attach(SERVO_PIN);


  Serial.begin(9600);
  SerialBT.begin("ESP32 ESP32");

  Serial.println("Device has been connected");
}

void getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // get the distance
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = (duration*.0343)/2; 

  Serial.print("Distance: ");
  Serial.println(distance);
}

void loop() {
    String input = "";

    // Check Bluetooth first
    if (SerialBT.available()) {
      input = SerialBT.readStringUntil('\n');
      Serial.println("[BT] " + input);  // <-- show it in Arduino Serial Monitor
      // Move the servo
      servo.write(0);
    }

    // Or check USB serial
    else if (Serial.available()) {
      input = Serial.readStringUntil('\n');
    }

    if (input.length() > 0) {
      getDistance();
      
      input.trim(); 
      Serial.println("Received: " + input);
      Serial.print("Distance: ");
      Serial.println(distance);
      servo.write(0);

      if (input == "scissor") {
        digitalWrite(LAMP, LOW);
        delay(200);
        digitalWrite(LAMP, HIGH);
        delay(200);
        digitalWrite(LAMP, LOW);

        // Move the servo
        servo.write(180);
      }
    }

    delay(100);
  }