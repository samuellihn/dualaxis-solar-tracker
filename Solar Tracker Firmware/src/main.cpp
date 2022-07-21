#include <Arduino.h>
#include <Servo.h>
#include <Adafruit_INA219.h>

#include "message.h"
uint16_t bottomLeftRaw, topLeftRaw, topRightRaw, bottomRightRaw;

Servo tilt, pan;

Adafruit_INA219 panelINA;

void readSunValues(PanelData &data);
void readServoPos(PanelData &data);
void readPanelPower(PanelData &data);

void setup()
{
    Serial.begin(115200);

    if (!panelINA.begin())
    {
        Serial.println("Failed to find INA219 chip");
        while (1) delay(10);
    }
    panelINA.setCalibration_16V_400mA();

    tilt.attach(5);
    tilt.write(90);
    pan.attach(6);
    pan.write(90);
}
PanelData data;

ServoPos cmd;
void loop()
{
    if (Serial.available())
    {
        cmd.recv();

        if (cmd.tilt <= 180) tilt.write(cmd.tilt);
        if (cmd.pan <= 180) pan.write(cmd.pan);
        readSunValues(data);
        readServoPos(data);
        readPanelPower(data);
        data.transmit();
    }
    delay(40);
}

void readSunValues(PanelData &data)
{
    topLeftRaw = analogRead(A3);
    topRightRaw = analogRead(A2);
    bottomLeftRaw = analogRead(A0); 
    bottomRightRaw = analogRead(A1);

    data.photoBL = bottomLeftRaw;
    data.photoBR = bottomRightRaw;
    data.photoTL = topLeftRaw;
    data.photoTR = topRightRaw;
}

void readPanelPower(PanelData &data)
{
    float shuntvoltage = panelINA.getShuntVoltage_mV();
    float busvoltage = panelINA.getBusVoltage_V();
    float current_mA = panelINA.getCurrent_mA();
    float power_mW = panelINA.getPower_mW();
    float loadvoltage = busvoltage + (shuntvoltage / 1000);

    data.panelVolt = busvoltage;
    data.panelAmp = current_mA;
    data.panelPwr = power_mW;

    delay(10);
}

void readServoPos(PanelData &data) {
    data.tilt = tilt.read();
    data.pan = pan.read();
}