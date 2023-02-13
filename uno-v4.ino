''' LIBRARIES & HEADERS '''
#include <DateTime.h>
#include <MPU6050.h>
#include <SoftwareSerial.h>
#include <Wire.h>

SoftwareSerial BLUETOOTH_SERIAL(0, 1); // RX, TX pins for HC-05

MPU6050 accel_gyro;

bool DOOR_HANDLE_STATE = false;
int AX, ay, AZ;
int GX, GY, GZ;
const int THRESHOLD = 15000;
const int ACCEL_X_THRESHOLD = 464;
const int ACCEL_Y_THRESHOLD = 15902;
const int ACCEL_Z_THRESHOLD = -2276;
const int GYRO_X_THRESHOLD = 119;
const int GYRO_Y_THRESHOLD = 149;
const int GYRO_Z_THRESHOLD = 375;
const int BUZZER_PIN = 6;
const int RED_PIN = 10;
const int GREEN_PIN = 11;
const int BLUE_PIN = 9;
const int MOTOR_PIN1 = 4;
const int MOTOR_PIN2 = 3;
const int ENABLE_PIN = 5;

void setup() {
    Wire.begin();
    accel_gyro.initialize();
    Serial.begin(9600);
    bluetooth_serial.begin(9600);

    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
    pinMode(MOTOR_PIN1, OUTPUT);
    pinMode(MOTOR_PIN2, OUTPUT);
    pinMode(ENABLE_PIN, OUTPUT);
}

void pair_bluetooth() {
  Serial.begin(9600);
  BLUETOOTH_SERIAL.begin(9600);

  // Attempt to pair with the Bluetooth module
  BLUETOOTH_SERIAL.print("AT");
  delay(500);
  if (BLUETOOTH_SERIAL.available()) {
    String response = BLUETOOTH_SERIAL.readString();
    if (response.startsWith("OK")) {
      Serial.println("Bluetooth module paired");
    } else {
      Serial.println("Failed to pair with Bluetooth module");
    }
  }
}

void run_bluetooth() {
  if (BLUETOOTH_SERIAL.available()) {
    char c = BLUETOOTH_SERIAL.read();
    Serial.write(c);
  }

  if (Serial.available()) {
    char c = Serial.read();
    BLUETOOTH_SERIAL.write(c);
  }
}


void display_status(float TEMPERATURE, bool SWITCH_STATE, bool PIR_STATE) {
  char CURRENT_TIME[20];
  sprintf(CURRENT_TIME, "%04d-%02d-%02d %02d:%02d:%02d", 
    year(), month(), day(), hour(), minute(), second());
  
  Serial.println(CURRENT_TIME);
  Serial.print("Temperature: ");
  Serial.println(TEMPERATURE);
  Serial.print("Switch State: ");
  Serial.println(SWITCH_STATE);
  Serial.print("PIR State: ");
  Serial.println(PIR_STATE);
}


''' FUNCTIONS TO HANDLE CONDITIONS '''
// Perform action for condition 0
void handle_condition_0() {
    Serial.printIn("Handling Condition 0")
}

void handle_condition_1() {
    Serial.printIn("Handling Condition 1")
}

void handle_condition_2() {
    Serial.printIn("Handling Condition 2")
}

void handle_condition_3() {
    Serial.printIn("Handling Condition 3")
}

void door_intrusion() {
    Serial.println("Intrusion detected!");
    bluetooth_serial.println("Intrusion detected!");
    tone(BUZZER_PIN, 2000);
    analogWrite(RED_PIN, 255);
    analogWrite(GREEN_PIN, 0);
    analogWrite(BLUE_PIN, 0);
    digitalWrite(MOTOR_PIN1, HIGH);
    digitalWrite(MOTOR_PIN2, LOW);
    analogWrite(ENABLE_PIN, 255);
    delay(3000);
}

void door_normal() {
    Serial.println("Door handle returned to normal position");
    bluetooth_serial.println("Door handle returned to normal position");
    noTone(BUZZER_PIN);
    analogWrite(RED_PIN, 0);
    analogWrite(GREEN_PIN, 0);
    analogWrite(BLUE_PIN, 0);
    analogWrite(ENABLE_PIN, 0);
    delay(1000);
}

void loop() {
    accel_gyro.getMotion6(&AX, &ay, &AZ, &GX, &GY, &GZ);
    bool NEW_STATE = (GX < GYRO_X_THRESHOLD - THRESHOLD || GX > GYRO_X_THRESHOLD + THRESHOLD) || (GY < GYRO_Y_THRESHOLD - THRESHOLD || GY > GYRO_Y_THRESHOLD + THRESHOLD) || (GZ < GYRO_Z_THRESHOLD - THRESHOLD || GZ > GYRO_Z_THRESHOLD + THRESHOLD) || (AX < ACCEL_X_THRESHOLD - THRESHOLD || AX > ACCEL_X_THRESHOLD + THRESHOLD) || (AY < ACCEL_Y_THRESHOLD - THRESHOLD || ay > ACCEL_Y_THRESHOLD + THRESHOLD) || (AZ < ACCEL_Z_THRESHOLD - THRESHOLD || AZ > ACCEL_Z_THRESHOLD + THRESHOLD);
    if (NEW_STATE != DOOR_HANDLE_STATE) {
        DOOR_HANDLE_STATE = NEW_STATE;
        if (DOOR_HANDLE_STATE) {
            door_intrusion();
        } else {
            door_normal();
        }
    }
    delay(200);
}
