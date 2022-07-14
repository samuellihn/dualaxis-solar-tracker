#include <Arduino.h>

struct ServoPos
{
    uint8_t pan;
    uint8_t tilt;

    void recv();
};

void ServoPos::recv()
{
    pan = Serial.parseInt();
    Serial.read();
    tilt = Serial.parseInt();
    Serial.read();
}

struct PanelData
{
    float panelVolt;
    float panelAmp;
    float panelPwr;

    uint16_t photoTR;
    uint16_t photoTL;
    uint16_t photoBR;
    uint16_t photoBL;

    uint8_t pan;
    uint8_t tilt;
    PanelData(){};

    PanelData(
        float v, float i, float p,
        uint16_t tr,
        uint16_t tl, uint16_t br, uint16_t bl,
        uint8_t pan, uint8_t tilt);

    void transmit();
};


PanelData::PanelData(
    float v, float i, float p,
    uint16_t tr,
    uint16_t tl, uint16_t br, uint16_t bl,
    uint8_t pan, uint8_t tilt) : panelVolt(v), panelAmp(i), panelPwr(p),
                                 photoTR(tr), photoTL(tl), photoBR(br), photoBL(bl),
                                 pan(pan), tilt(tilt){};

void PanelData::transmit()
{
    Serial.print("?");
    Serial.print(panelVolt);
    Serial.print(",");
    Serial.print(panelAmp);
    Serial.print(",");
    Serial.print(panelPwr);
    Serial.print("|");

    Serial.print(photoTR);
    Serial.print(",");
    Serial.print(photoTL);
    Serial.print(",");
    Serial.print(photoBR);
    Serial.print(",");
    Serial.print(photoBL);
    Serial.print("|");

    Serial.print(pan);
    Serial.print(",");
    Serial.println(tilt);
}