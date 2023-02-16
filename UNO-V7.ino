#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <MPU6050.h>

#define ADS1115_ADDRESS 0x48

#define PIN_SWITCH 2
#define PIN_PIR 3
#define PIN_BUZZER 4
#define PIN_RELAY 5
#define PIN_LED 6
#define PIN_MOTOR 9

#define TEMPERATURE_THRESHOLD 26

class TimestampedPrinter {
public:
    void print_with_timestamp(String message) {
        String timestamp = "[" + String(millis()) + "]";
        Serial.println(timestamp + " " + message);
    }
};

TimestampedPrinter tp;

MPU6050 accel_gyro;

Adafruit_ADS1115 ads;

float max_voltage = 3.3;

int relay_state = 0;

void setup() {
    Serial.begin(9600);
    Serial1.begin(9600);
    tp.print_with_timestamp("Initialising system...");
    pinMode(PIN_SWITCH, INPUT);
    pinMode(PIN_PIR, INPUT);
    pinMode(PIN_BUZZER, OUTPUT);
    pinMode(PIN_RELAY, OUTPUT);
    pinMode(PIN_LED, OUTPUT);
    pinMode(PIN_MOTOR, OUTPUT);
    ads.begin(ADS1115_ADDRESS);
    tp.print_with_timestamp("System initialized.");
}



void write_buzzer_state(int state) {
    Serial1.println("BUZZER_STATE:" + String(state));
}

void write_led_state(int state) {
    Serial1.println("LED_STATE:" + String(state));
}

void write_motor_state(int state) {
    Serial1.println("MOTOR_STATE:" + String(state));
}

void write_relay_state(int state) {
    digitalWrite(PIN_RELAY, state);
    relay_state = state;
    Serial1.println("RELAY_STATE:" + String(state));
}

void determine_outputs(int temperature_state, int switch_state, int gyro_state, int pir_state) {
    int outputs[4] = {0, 0, 0, 0};
    if (temperature_state == 1 && switch_state == 1 && gyro_state == 1) {
        outputs[0] = 1;
    }
    if (switch_state == 1) {
        outputs[1] = 1;
    }
    if (gyro_state == 1) {
        outputs[2] = 1;
    }
    if (pir_state == 1) {
        outputs[3] = 1;
    }
    Serial1.print("OUTPUTS:");
    for (int i = 0; i < 4; i++) {
        Serial1.print(outputs[i]);
        if (i < 3) {
            Serial1.print(",");
        }
    }
    Serial1.println();
    tp.print_with_timestamp("Determining output values...");
}

void write_ALL_outputs() {
    if (Serial1.available() > 0) {
        String input_str = Serial1.readStringUntil('\n');
        input_str.trim();
        String inputs[4];
        int start_index = 0;
        for (int i = 0; i < input_str.length(); i++) {
            if (input_str.charAt(i) == ':') {
                inputs[i] = input_str.substring(start_index, i);
                start_index = i + 1;
            }
        }
        inputs[3] = input_str.substring(start_index);
        int outputs[4];
        start_index = 0;
        for (int i = 0; i < 4; i++) {
            int end_index = inputs[i].indexOf(",", start_index);
            if (end_index == -1) {
                end_index = inputs[i].length();
            }
            outputs[i] = inputs[i].substring(start_index, end_index).toInt();
            start_index = end_index + 1;
        }
        if (outputs[1] == 1) {
            write_buzzer_state(1);
        } else {
            write_buzzer_state(0);
        }
        if (outputs[2] == 1) {
            write_led_state(1);
        } else {
            write_led_state(0);
        }
        if (outputs[3] == 1) {
            write_motor_state(1);
        } else {
            write_motor_state(0);
        }
        if (outputs[0] == 1) {
            write_relay_state(1);
        } else {
            write_relay_state(0);
        }
        tp.print_with_timestamp("Writing output values...");
    }
}

// Write the values of all outputs to their respective destinations
void write_ALL_outputs() {
    tp.print_with_timestamp("Writing output values...");
    write_relay_state(outputs[0]);
    write_buzzer_state(outputs[1]);
    write_led_state(outputs[2]);
    write_motor_state(outputs[3]);
    if (Serial1.available() > 0) {
        String input_str = Serial1.readStringUntil('\n');
        input_str.trim();
        String inputs[4];
        int start_index = 0;
        for (int i = 0; i < 4; i++) {
            int end_index = input_str.indexOf(",", start_index);
            if (end_index == -1) {
                end_index = input_str.length();
            }
            inputs[i] = input_str.substring(start_index, end_index);
            start_index = end_index + 1;
        }
        int outputs[4];
        for (int i = 0; i < 4; i++) {
            outputs[i] = inputs[i].toInt();
        }
    }
}

// Main program loop
void loop() {
    // Read input values from various sources
    int temperature_state = read_temperature_state();
    int switch_state = read_switch_state(PIN_SWITCH);
    int gyro_state = read_gyro_state();
    int pir_state = read_pir_state();

    // Determine the output values based on the input values and a set of conditions
    determine_outputs(temperature_state, switch_state, gyro_state, pir_state);

    // Write the values of all outputs to their respective destinations
    write_ALL_outputs();
}
