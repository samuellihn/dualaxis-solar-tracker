#include <Servo.h>
 Servo panelTrackerX;
 Servo panelTrackerY;
 int TLLDRPin = 0;
 int TRLDRPin = 1;
 int BRLDRPin = 2;
 int BLLDRPin = 3;
CHANGE PIN NUMBER
 int LdrTR = 0;
 int LdrTL = 0;
 int LdrBR = 0;
 int LdrBL = 0;
 int avgTop = 0;
 int avgBot = 0;
 int avgRig = 0;
 int avgLef = 0;
 int Ydiff = 0;
 int Xdiff = 0;
 int trackerXPos = 90;
 int trackerYPos = 90;
int totalLDR = 0;
void setup() {
  panelTrackerX.attach(5);
  panelTrackerY.attach(6);
  //CHANGE NUMBER TO SERVO PIN
}

void loop() {
  LdrTR = analogRead(TRLDRPin);
  LdrTL = analogRead(TLLDRPin);
  LdrBL = analogRead(BLLDRPin);
  LdrBR = analogRead(BRLDRPin);
  avgTop = (LdrTR + LdrTL)/2;
  avgBot = (LdrBR + LdrBL)/2;
  avgRig = (LdrTR + LdrBR)/2;
  avgLef = (LdrTL + LdrBL)/2;
  Ydiff = (avgTop - avgBot);
  Xdiff = (avgRig - avgLef);
  totalLDR = (avgTop + avgBot + avgRig + avgBot);
  When it is dark out, the solar panel goes to the east and leans down. Waits for Sunrise
  if (totalLDR < 8)
  {
    while(trackerXPos<=160)
    //DOUBLECHECKNUMBER
    {
      trackerXPos++;
      panelTrackerX.write(trackerXPos);
      delay(100);
    }
    while(trackerYPos<=160)
    //DOUBLE CHECK NUMBER
    {
      trackerYPos++;
      panelTrackerY.write(trackerYPos);
      delay(100);
    }
  }
  Checks the X and Y differences
  Ydiff = (avgTop - avgBot);
  Xdiff = (avgRig - avgLef);
  if top Y is bigger than bottom, then tilt towards topY
  if(Ydiff>15){
    if(trackerYPos<=160)
    {
      trackerYPos++;
      panelTrackerY.write(trackerYPos);
    }
  }
  else if(Ydiff<-15){
    if(trackerYPos>20)
    {
      trackerYPos--;
      panelTrackerY.write(trackerYPos);
    }
  }
  if(Xdiff>15){
    if(trackerXPos<=160)
    {
      trackerXPos++;
      panelTrackerX.write(trackerXPos);
    }
  }
  else if(Xdiff<-15){
    if(trackerXPos>20)
    {
      trackerXPos--;
      panelTrackerX.write(trackerXPos);
    }
  }
  delay(100);
  }
