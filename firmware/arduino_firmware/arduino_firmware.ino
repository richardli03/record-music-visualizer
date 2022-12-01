/* Arduino-side firmware for GPIO motor control
using DRV8825 stepper drivers and a L298N H-bridge for the DC motor.
pins listed below for sanity:

Stepper Motor A:
DIR (blue)  -> pin 8
STP (green) -> pin 9

Stepper Motor B:
DIR (blue)  -> pin 10
STP (green) -> pin 11

Stepper Motor C:
DIR (blue)  -> pin 12
STP (green) -> pin 13

DC Motor
IN 1 (mark) -> pin 4
IN 2 (blue) -> pin 2
ENB (black) -> pin 3 (pwm)
*/

#include <Arduino.h>
#include <L298N.h>
#include <AccelStepper.h>

// *** DC motor setup ***
const unsigned int IN1 = 4;
const unsigned int IN2 = 2;
const unsigned int EN = 3;
L298N DCmotor(EN, IN1, IN2);

// *** stepper motor setup ***
AccelStepper stepperA(AccelStepper::DRIVER, 9, 8);    // stp = 9, dir = 8
AccelStepper stepperB(AccelStepper::DRIVER, 11, 10);  // stp = 11, dir = 10
AccelStepper stepperC(AccelStepper::DRIVER, 13, 12);  // stp = 13, dir = 12


void setup() {
  // initialize serial communication
  Serial.begin(115200);

  // maximum speed in steps per second
  stepperA.setMaxSpeed(1100);
  stepperB.setMaxSpeed(1100);
  stepperC.setMaxSpeed(1100);
}


void loop() {
  // if a stepper has a target destination remaining, step 1 step
  stepperA.runSpeedToPosition();
  stepperB.runSpeedToPosition();
  stepperC.runSpeedToPosition();

  // *** check and process serial command if needed ***
  String command;
  if (Serial.available() != 0) {  // if data available in serial receive buffer
    // commands start with '(' and end with ')' to avoid garbage characters
    if (Serial.read() == '(') {
      command = Serial.readStringUntil(')');
      Serial.println(command);

      // A stepper
      if (command.startsWith("sa")) {
        long steps = command.substring(2, command.length()).toInt();
        // move stepper `steps` steps
        stepperA.move(steps);     // set relative target position
        stepperA.setSpeed(1100);  // must set speed after moveTo to get rid of accl
      }
      // B stepper
      else if (command.startsWith("sb")) {
        long steps = command.substring(2, command.length()).toInt();
        // move stepper `steps` steps
        stepperB.move(steps);     // set relative target position
        stepperB.setSpeed(1100);  // must set speed after moveTo to get rid of accl
      }
      // C stepper
      else if (command.startsWith("sc")) {
        long steps = command.substring(2, command.length()).toInt();
        // move stepper `steps` steps
        stepperC.move(steps);     // set relative target position
        stepperC.setSpeed(1100);  // must set speed after moveTo to get rid of accl
      }
      // DC motor run with `drN` where N is speed between 0-255
      else if (command.startsWith("dr")) {
        unsigned short speed = command.substring(2, command.length()).toInt();
        DCmotor.setSpeed(speed);
        DCmotor.forward();

        // stop DC motor with `ds`
      } else if (command == "ds") {
        DCmotor.setSpeed(0);
        DCmotor.forward();
      }
    }
  }
}