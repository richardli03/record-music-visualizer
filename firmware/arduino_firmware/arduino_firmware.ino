/* Arduino-side firmware for GPIO motor control
using DRV8825 stepper drivers and a L298N H-bridge for the DC motor.
pins listed below for sanity:

Stepper Motor 1:
DIR (blue)  -> pin 8
STP (green) -> pin 9

Stepper Motor 2
DIR (blue)  -> pin 10
STP (green) -> pin 11

Stepper Motor 3
DIR (blue)  -> pin 12
STP (green) -> pin 13

DC Motor
IN 1 (mark) -> pin 4
IN 2 (blue) -> pin 2
ENB (black) -> pin 3 (pwm)
*/

#include <Arduino.h>
#include <L298N.h>
#include "BasicStepperDriver.h"

// *** DC motor setup ***
const unsigned int IN1 = 4;
const unsigned int IN2 = 2;
const unsigned int EN = 3;
L298N DCmotor(EN, IN1, IN2);

// *** stepper motor setup ***
#define MOTOR_STEPS 200  // motor steps per full revolution (200 steps or 1.8 degrees/step)
#define RPM 120          // rotations per minute
#define MICROSTEPS 1     // microstepping (1 = full step aka no microstepping)

// stepper 1
#define DIR1 8
#define STEP1 9
BasicStepperDriver stepper1(MOTOR_STEPS, DIR1, STEP1);

// stepper 2
#define DIR2 10
#define STEP2 11
BasicStepperDriver stepper2(MOTOR_STEPS, DIR2, STEP2);

// stepper 3
#define DIR3 12
#define STEP3 13
BasicStepperDriver stepper3(MOTOR_STEPS, DIR3, STEP3);

//
void setup() {
  // initialize serial communication
  Serial.begin(115200);
  stepper1.begin(RPM, MICROSTEPS);
  stepper2.begin(RPM, MICROSTEPS);
  stepper3.begin(RPM, MICROSTEPS);
}
void loop() {
  String command;
  while (Serial.available() == 0) {
    // wait for data available in serial receive buffer
  }
  // commands start with '(' and end with ')' to avoid garbage characters
  if (Serial.read() == '(') {
    command = Serial.readStringUntil(')');
    Serial.println(command);
    // DC motor run with `drN` where N is speed between 0-255
    if (command.startsWith("dr")) {
      unsigned short speed = command.substring(2, command.length()).toInt();
      DCmotor.setSpeed(speed);
      DCmotor.forward();
      // stop DC motor with `ds`
    } else if (command == "ds") {
      DCmotor.setSpeed(0);
      DCmotor.forward();
    }
    // set stepper motor rotation with `saN` where N is degrees of rotation and
    // characters a-c refers to motors 1-3 repectivly
    else if (command.startsWith("sa")) {
      int deg = command.substring(2, command.length()).toInt();
      stepper1.rotate(deg);
    }
    else if (command.startsWith("sb")) {
      int deg = command.substring(2, command.length()).toInt();
      stepper2.rotate(deg);
    }
    else if (command.startsWith("sc")) {
      int deg = command.substring(2, command.length()).toInt();
      stepper3.rotate(deg);
    }
  }
}