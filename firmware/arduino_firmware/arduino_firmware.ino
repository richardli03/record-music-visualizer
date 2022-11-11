/* Arduino-side firmware for GPIO motor control
using DRV8825 stepper drivers and a L298N H-bridge for the DC motor.

pins listed below for sanity:

stepper motor 1:
STP -> pin 9
DIR -> pin 8

stepper motor 2
STP -> pin 6
DIR -> pin 7

stepper motor 3
STP -> pin 5
DIR -> pin 4

DC motor
IN 1 -> pin 1
IN 2 -> pin 3
ENB -> pin 2 (pwm)
*/

#include <Arduino.h>
#include <L298N.h>
#include "BasicStepperDriver.h"

// *** DC motor setup ***
const unsigned int IN1 = 1;
const unsigned int IN2 = 3;
const unsigned int EN = 2;
L298N DCmotor(EN, IN1, IN2);

// *** stepper motor setup ***

// Motor steps per full revolution (200 steps or 1.8 degrees/step)
#define MOTOR_STEPS 200
#define RPM 120
// microstepping (1 = full step aka no microstepping)
#define MICROSTEPS 1

// stepper 1
#define DIR1 8
#define STEP1 9
BasicStepperDriver stepper1(MOTOR_STEPS, DIR1, STEP1);

void setup() {
  // initialize serial communication
  Serial.begin(115200);
  stepper1.begin(RPM, MICROSTEPS);
}
void loop() {
  while (Serial.available() == 0) {
    // wait for data available in serial receive buffer
  }
  String command = Serial.readStringUntil('\n');  // read until timeout
  Serial.print(command);
    // set stepper motor rotation with `s1 N` where N is degrees of rotation
  if (command.startsWith("s1")) {
    int deg = command.substring(command.indexOf(" ") + 1, command.length()).toInt();
    stepper1.rotate(deg);

    // set DC motor speed with `dc N` where N between 0-255
  } else if (command.startsWith("dc")) {
    unsigned short speed = command.substring(command.indexOf(" ") + 1, command.length()).toInt();
    DCmotor.setSpeed(speed);
    DCmotor.forward();
    Serial.println(speed);
    
    // stop DC motor with `ds`
  } else if (command == "ds") {
    DCmotor.setSpeed(0);
    DCmotor.forward();
    Serial.println("STOP");
  }
}