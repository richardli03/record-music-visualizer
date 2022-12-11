// arduino sketch to test DC motor over serial

#include <L298N.h>

// Pin definition
const unsigned int IN1 = 1;
const unsigned int IN2 = 3;
const unsigned int EN = 2;

// motor instance
L298N motor(EN, IN1, IN2);

void setup()
{
  // Used to display information
  Serial.begin(115200);

  // Wait for Serial Monitor to be opened
  while (!Serial)
  {
    //do nothing
  }

  // // Set initial speed
  // motor.setSpeed(200);
}

void loop()
{

 while (Serial.available() == 0) {
    // wait for data available in serial receive buffer
  }
  String command = Serial.readStringUntil('\n');  // read until timeout
  Serial.print(command);
  if (command.startsWith("r")) {
    unsigned short speed = command.substring(command.indexOf(" ") + 1, command.length()).toInt();
    motor.setSpeed(speed);
    motor.forward();
    Serial.println(speed);
    
  } else if (command == "stop") {
    motor.setSpeed(0);
    motor.forward();
    Serial.println("STOP");
  }
}