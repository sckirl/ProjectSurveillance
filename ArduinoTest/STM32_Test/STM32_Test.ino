#define BUZZER PB12

void setup() {
  pinMode(BUZZER, OUTPUT);
  Serial.begin(19200);

  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);

  Serial.println("Device has been connected");
}

void loop() {
  String input = "";

  Serial.println("test");

  if (Serial.available()) {
    input = Serial.readStringUntil('\n');

    Serial.print("the input is: ");
    Serial.println(input);

    if(input == "test"){ 
      digitalWrite(BUZZER, LOW);
      delay(100);
      digitalWrite(BUZZER, HIGH);
      delay(100);
    }
  } 

  delay(100);
}