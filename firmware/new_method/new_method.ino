// testing the AccelStepper library
#include <AccelStepper.h>

/*
Stepper Motor A:
DIR (blue)  -> pin 8
STP (green) -> pin 9

Stepper Motor B:
DIR (blue)  -> pin 10
STP (green) -> pin 11

Stepper Motor C:
DIR (blue)  -> pin 12
STP (green) -> pin 13
*/

// define steppers and pins
AccelStepper stepperA(AccelStepper::DRIVER, 9, 8);    // stp = 9, dir = 8
AccelStepper stepperB(AccelStepper::DRIVER, 11, 10);  // stp = 11, dir = 10
AccelStepper stepperC(AccelStepper::DRIVER, 13, 12);    // stp = 13, dir = 12


void setup() {
  // serial baud rate 115200
  Serial.begin(115200);

  // maximum speed in steps per second
  stepperA.setMaxSpeed(1100);
  stepperB.setMaxSpeed(1100);
  stepperC.setMaxSpeed(1100);
}


void loop() {
  // step steppers 1 step if needed
  stepperA.runSpeedToPosition();
  stepperB.runSpeedToPosition();
  stepperC.runSpeedToPosition();

  // check/ process serial command
  String command;
  if (Serial.available() != 0) { // if data available in serial receive buffer
    // commands start with '(' and end with ')' to avoid garbage characters
    if (Serial.read() == '(') {
      command = Serial.readStringUntil(')');
      Serial.println(command);

      // A stepper
      if (command.startsWith("sa")) {
        long steps = command.substring(2, command.length()).toInt();
        // move stepper `steps` steps
        stepperA.moveTo(stepperA.currentPosition() + steps); // set target position
        stepperA.setSpeed(1100);  // must set speed after moveTo to get rid of accl
      }
      // B stepper
      else if (command.startsWith("sb")) {
        long steps = command.substring(2, command.length()).toInt();
        // move stepper `steps` steps
        stepperB.moveTo(stepperB.currentPosition() + steps); // set target position
        stepperB.setSpeed(1100);  // must set speed after moveTo to get rid of accl
      }
      // C stepper
      else if (command.startsWith("sc")) {
        long steps = command.substring(2, command.length()).toInt();
        // move stepper `steps` steps
        stepperC.moveTo(stepperC.currentPosition() + steps); // set target position
        stepperC.setSpeed(1100);  // must set speed after moveTo to get rid of accl
      }
    }
  }
}