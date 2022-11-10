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
ENB -> pin 2
IN 4 -> pin 3
*/

#include <Arduino.h>
#include <L298N.h>
#include "BasicStepperDriver.h"

// stepper motor steps per revolution (200 steps = 1.8 degrees/step)
#define MOTOR_STEPS 200
#define RPM 120
// microstepping not set externally (1 = full step)
#define MICROSTEPS 1

// define wires
#define DIR1 8
#define STEP1 9


// global variables
String command;

void setup() {
  // initialize serial communication
  Serial.begin(115200);

}


void loop() {
readSerialBuffer();

}


// **funtions defined below this point**

// read serial and update command string
void readSerialBuffer() {
  while (Serial.available() == 0) {
    // wait for data available in serial receive buffer
  }
  command = Serial.readStringUntil('\n');  // read until timeout
  command.trim();                          // remove white space or \n
}