// arduino sketch to verify the stepper motor connected to pins 8 and 9 works
// as expected over serial

#include <Arduino.h>
#include "BasicStepperDriver.h"

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
#define RPM 120

// microstepping (1 = full step aka no microstepping)
#define MICROSTEPS 1

// wires
#define DIR 8
#define STEP 9

// 2-wire basic config, microstepping is hardwired on the driver
BasicStepperDriver stepper(MOTOR_STEPS, DIR, STEP);

void setup() {
  // initialize serial communication
  Serial.begin(115200);
  stepper.begin(RPM, MICROSTEPS);
}

void loop() {
  while (Serial.available() == 0) {
    // wait for data available in serial receive buffer
  }
  String command = Serial.readStringUntil('\n');  // read until timeout
  Serial.print(command);
  if (command.startsWith("s1")) {
    int steps = command.substring(command.indexOf(" ")+1, command.length()).toInt();
    stepper.rotate(steps);
  }
}