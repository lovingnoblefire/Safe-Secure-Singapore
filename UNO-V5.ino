#include <Arduino.h>
#include <MPU6050.h>

MPU6050 accel_gyro;

// Define the function that prints the timestamp and the message
void print_with_timestamp(String message) {
  char timestamp[20];
  sprintf(timestamp, "[%04d-%02d-%02d @ %02d:%02d:%02d] ", year(), month(), day(), hour(), minute(), second());
  Serial.print(timestamp);
  Serial.println(message);
}

// Define the constants for the condition handlers
const String condition0 = "CONDITION_0";
const String condition1 = "CONDITION_1";
const String condition2 = "CONDITION_2";
const String condition3 = "CONDITION_3";

bool check_door_handle_state(int gyro_x_threshold, int gyro_y_threshold, int gyro_z_threshold, int threshold) {
  int AX, AY, AZ, GX, GY, GZ;
  accel_gyro.getMotion6(&AX, &AY, &AZ, &GX, &GY, &GZ);
  bool door_handle_moved = (GX < gyro_x_threshold - threshold || GX > gyro_x_threshold + threshold) ||
                           (GY < gyro_y_threshold - threshold || GY > gyro_y_threshold + threshold) ||
                           (GZ < gyro_z_threshold - threshold || GZ > gyro_z_threshold + threshold);
  return door_handle_moved;
}



// Define the condition handlers
void handle_condition_0() {
  print_with_timestamp("Condition 0 detected, performing action...");
  // Turn off the relay connected to the door lock
  // TODO: insert code to turn off the relay connected to the door lock here

  // Turn off the buzzer
  // TODO: insert code to turn off the buzzer here

  // Turn off the LED
  // TODO: insert code to turn off the LED here

  // Stop the motor connected to the door handle
  // TODO: insert code to stop the motor connected to the door handle here
  print_with_timestamp("End of Condition 0");
}

void handle_condition_1() {
  print_with_timestamp("Condition 1 detected, performing action...");
  // Turn on the relay connected to the door lock
  // TODO: insert code to turn on the relay connected to the door lock here

  // Turn off the buzzer
  // TODO: insert code to turn off the buzzer here

  // Turn off the LED
  // TODO: insert code to turn off the LED here

  // Stop the motor connected to the door handle
  // TODO: insert code to stop the motor connected to the door handle here

  print_with_timestamp("End of Condition 1");
}

void handle_condition_2() {
  print_with_timestamp("Condition 2 detected, performing action...");
  // Turn on the LED
  // TODO: insert code to turn on the LED here

  // Start the motor connected to the door handle
  // TODO: insert code to start the motor connected to the door handle here

  // Turn off the relay connected to the door lock
  // TODO: insert code to turn off the relay connected to the door lock here

  // Turn off the buzzer
  // TODO: insert code to turn off the buzzer here

  print_with_timestamp("End of Condition 2");
}

void handle_condition_3() {
  print_with_timestamp("Condition 3 detected, performing action...");
  // Turn off the relay connected to the door lock
  // TODO: insert code to turn off the relay connected to the door lock here

  // Turn on the buzzer
  // TODO: insert code to turn on the buzzer here

  // Turn on the LED
  // TODO: insert code to turn on the LED here

  // Stop the motor connected to the door handle
  // TODO: insert code to stop the motor connected to the door handle here

  print_with_timestamp("End of Condition 3");
}



void setup() {
  Serial.begin(9600);
  accel_gyro.initialize();
}


void loop() {
  // Check for incoming data from the Raspberry Pi
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil(':');
    String argument = Serial.readStringUntil('\n');

    // Check that the command and argument are not empty
    if (command.length() == 0 || argument.length() == 0) {
      print_with_timestamp("Invalid command or argument");
      return;
    }

    // Call the appropriate condition handler based on the command
    if (command == condition0) {
      handle_condition_0();
    } else if (command == condition1) {
      handle_condition_1();
    } else if (command == condition2) {
      handle_condition_2();
    } else if (command == condition3) {
      handle_condition_3();
    } else {
      print_with_timestamp("Invalid command: " + command);
    }
  }
}
