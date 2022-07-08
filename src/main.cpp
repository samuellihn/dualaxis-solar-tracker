#include <Arduino.h>
#include <Braccio.h>      //Required for Braccio Robotic Arm
#include <Servo.h>        //Required for Braccio Robotic Arm servo processing
#include <InverseK.h>

/****************************************************************
*  Use Arduino 1.8.9 IDE
*****************************************************************/

String inStringM1 = "";    // string to hold passed VALUE input
String inStringM2 = "";    // string to hold passed VALUE input
String inStringM3 = "";    // string to hold passed VALUE input
String inStringM4 = "";    // string to hold passed VALUE input
String inStringM5 = "";    // string to hold passed VALUE input
String inStringM6 = "";    // string to hold passed VALUE input
int M1Value = 999;          // initialize Value number passed from Python, used after conversion of string to integer.
int M2Value = 999;          // initialize Value number passed from Python, used after conversion of string to integer.
int M3Value = 999;          // initialize Value number passed from Python, used after conversion of string to integer.
int M4Value = 999;          // initialize Value number passed from Python, used after conversion of string to integer.
int M5Value = 999;          // initialize Value number passed from Python, used after conversion of string to integer.
int M6Value = 999;          // initialize Value number passed from Python, used after conversion of string to integer.
int oldBaseVal = 90;          // initialize the Base resting postion in degrees. It can take values between 0 ~ 180.
int oldShoulderVal = 45;     // initialize the Shoulder resting postion in degrees. It can take values between 0 ~ 180.
int oldElbowVal = 180;          // initialize the Elbow resting postion in degrees. It can take values between 0 ~ 180.
int oldWristVerVal = 180;       // initialize the Wrist1 resting postion in degrees. It can take values between 0 ~ 180.
int oldWristRotVal = 90;      // initialize the Wrist2 resting postion in degrees. It can take values between 0 ~ 180.
int oldGripperVal = 10;       // initialize the Gripper open postion in degrees. It can take values between 10 ~ 73.
 

// Setup the servos types by name...
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_ver;
Servo wrist_rot;
Servo gripper;


// Quick conversion from the Braccio angle system to radians
float b2a(float b){
  return b / 180.0 * PI - HALF_PI;
}

// Quick conversion from radians to the Braccio angle system
float a2b(float a) {
  return (a + HALF_PI) * 180 / PI;
}

void setup();
void loop();
void moveArm(int baseVar, int shoulderVar, int elbowVar, int wrist1Var, int wrist2Var, int gripperVar);
//***************************** SETUP *********************************************
void setup() {

  Serial.begin(9600);           //initialize serial COM at 9600 baudrate. Sets the data rate in bits per second (baud) for serial data transmission.

  while (!Serial) {
    ;                           // wait for serial port to connect. Needed for native USB
  }//end while

  Serial.setTimeout(4000);      //setup the Serial port timeout long enough to get data from Python, >4 seconds.
  pinMode(13, OUTPUT);          //setup the LED pin

  digitalWrite(13, LOW);        //turn LED off.


  Link base, upperarm, forearm, hand;

  base.init(0, b2a(0.0), b2a(180.0));
  upperarm.init(200, b2a(15.0), b2a(165.0));
  forearm.init(200, b2a(0.0), b2a(180.0));
  hand.init(270, b2a(0.0), b2a(180.0));

  // Attach the links to the inverse kinematic model
  InverseK.attach(base, upperarm, forearm, hand);

  float a0, a1, a2, a3;

  // InverseK.solve() return true if it could find a solution and false if not.

  // Calculates the angles without considering a specific approach angle
  // InverseK.solve(x, y, z, a0, a1, a2, a3)
  Braccio.begin();
  if(InverseK.solve(200, 0, 50, a0, a1, a2, a3)) {
    Serial.print(a2b(a0)); Serial.print(',');
    Serial.print(a2b(a1)); Serial.print(',');
    Serial.print(a2b(a2)); Serial.print(',');
    Serial.println(a2b(a3));

  } else {
    Serial.println("No solution found!");
  }
  moveArm(a2b(a0), a2b(a1), a2b(a2), a2b(a3), 90, 10 );


  // //Initialization functions and set up the initial position for Braccio
  // //All the servo motors will be positioned in the "safety" position:
  // //Base (M1):90 degrees
  // //Shoulder (M2): 45 degrees
  // //Elbow (M3): 180 degrees
  // //Wrist vertical (M4): 180 degrees
  // //Wrist rotation (M5): 90 degrees
  // //gripper (M6): 10 degrees
  // Braccio.begin();                //Sets the data rate in bits per second (baud) for data transmission.

  // moveArm(90, 45, 180, 180, 90, 10);     //initialize arm in 'resting' position.
  
}


//***************************** LOOP ******************************************
void loop() {

  //NOTE: May need to use Strtoinit() to convert string to integer!!!
  /*########################################################################################
    #                                     
    #                                     M1 Base
    #                                     M2 Shoulder
    #                                     M3 Elbow
    #                                     M4 Wrist vertical
    #                                     M5 Wrist rotation
    #                                     M6 Gripper
    #
    #########################################################################################*/ 

  //****** Take Action ******
  // digitalWrite(13, HIGH);                         //Turn ON the LED.
  // moveArm(45, 90, 90, 90, 45, 72);
  // moveArm(90, 45, 180, 180, 90, 10);
  // //moveArm(M1Value, M2Value, M3Value, M4Value, M5Value, M6Value);
  // digitalWrite(13, LOW);                          //turn the LED off.

}

//************************************ MOVE ARM ***************************************************
// This function will move the Braccio Robotic Arm x number of degrees based on the passed values.
//*************************************************************************************************
void moveArm(int baseVar, int shoulderVar, int elbowVar, int wrist1Var, int wrist2Var, int gripperVar) {

  /*
  Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
  M1=base degrees. Allowed values from 0 to 180 degrees
  M2=shoulder degrees. Allowed values from 15 to 165 degrees
  M3=elbow degrees. Allowed values from 0 to 180 degrees
  M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
  M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
  M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */

  //(step delay, M1, M2, M3, M4, M5, M6); Do NOT open/close gripper.
  Braccio.ServoMovement(20, baseVar, shoulderVar, elbowVar, wrist1Var, wrist2Var, gripperVar);


  delay(1000);       //Wait 1 second for the servos to move into position.

}//end moveArm


