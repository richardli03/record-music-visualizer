// testing the AccelStepper library
#include <AccelStepper.h>

/*
Stepper Motor 1:
DIR (blue)  -> pin 8
STP (green) -> pin 9

Stepper Motor 2
DIR (blue)  -> pin 10
STP (green) -> pin 11

Stepper Motor 3
DIR (blue)  -> pin 12
STP (green) -> pin 13
*/

// define steppers and pins
AccelStepper stepper1(AccelStepper::DRIVER, 9, 8);    // stp = 9, dir = 8
AccelStepper stepper2(AccelStepper::DRIVER, 11, 10);  // stp = 11, dir = 10
AccelStepper stepper3(AccelStepper::DRIVER, 9, 8);    // stp = 13, dir = 13

void setup() {
  Serial.begin(115200);
  // maximum speed in steps per second
  stepper1.setMaxSpeed(3000);  // limits the value of setSpeed()
  
  // need to set target position as current position?

  // stepper2.setMaxSpeed(300.0);
  // stepper3.setMaxSpeed(300.0);
}


void loop() {
  // move stepper a lil
  stepper1.runSpeedToPosition();

  String command;
  if (Serial.available() != 0) { // if data available in serial receive buffer

    // commands start with '(' and end with ')' to avoid garbage characters
    if (Serial.read() == '(') {
      command = Serial.readStringUntil(')');
      Serial.println(command);

      // stepper
      if (command.startsWith("st")) {
        long steps = command.substring(2, command.length()).toInt();
        // set target position
        stepper1.moveTo(stepper1.currentPosition() + steps);
        // set speed so there's no acceleration
        stepper1.setSpeed(1100);
      }
    }
  }
}