// arduino sketch to verify the stepper motor connected to pins 8 and 9 works
// as expected

# include <Arduino.h>
#include "BasicStepperDriver.h"

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
#define RPM 120

// microstepping not set externally (1 = full step)
#define MICROSTEPS 1

// All the wires needed for full functionality
#define DIR 8
#define STEP 9
//Uncomment line to use enable/disable functionality
//#define SLEEP 13

// 2-wire basic config, microstepping is hardwired on the driver
BasicStepperDriver stepper(MOTOR_STEPS, DIR, STEP);

//Uncomment line to use enable/disable functionality
//BasicStepperDriver stepper(MOTOR_STEPS, DIR, STEP, SLEEP);

void setup() {
    stepper.begin(RPM, MICROSTEPS);
    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    // stepper.setEnableActiveState(LOW);
}

void loop() {
  
    // energize coils - the motor will hold position
    // stepper.enable();
  
    /*
     * Moving motor one full revolution using the degree notation
     */
    stepper.rotate(360);

    /*
     * Moving motor to original position using steps
     */
    stepper.move(-MOTOR_STEPS*MICROSTEPS);

    // pause and allow the motor to be moved by hand
    // stepper.disable();

    delay(5000);
}