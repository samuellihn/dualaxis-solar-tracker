#include <Arduino.h>
#include <Servo.h>
uint16_t bottomLeftRaw, topLeftRaw, topRightRaw, bottomRightRaw;

Servo tilt;
void readSunValues();
void setup()
{
  tilt.attach(5);
  tilt.write(90);

  Serial.begin(9600);
}

void loop()
{
  tilt.write(60);
  Serial.println(tilt.read());
  delay(1000);
  tilt.write(120);
  Serial.println(tilt.read());
  delay(1000);
}

void readSunValues() {

  // Bottom Left: A0
  // Top Left: A1
  // Top Right: A2
  // Bottom Right: A3
  bottomLeftRaw = analogRead(A0);
  topLeftRaw= analogRead(A1);
  topRightRaw = analogRead(A2);
  bottomRightRaw = analogRead(A3);
  Serial.print(bottomLeftRaw); Serial.print("|");
  Serial.print(topLeftRaw); Serial.print("|");
  Serial.print(topRightRaw); Serial.print("|");
  Serial.println(bottomRightRaw);
}