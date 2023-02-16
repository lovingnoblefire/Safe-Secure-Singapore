import datetime
import math
import serial
from adafruit_ads1x15.ads1115 import ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio
import gpiozero as GPIO

# GPIO Pin Numbers
PIR_PIN = 18
RELAY_PIN = 22
SWITCH_PIN = 26

# Set the GPIO mode to use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up the PIR sensor, the relay and the switch
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create the I2C bus
I2C_BUS = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(I2C_BUS)
MAX_VOLTAGE = 3.3

# Create single-ended input on channel 0
ADC_0 = AnalogIn(ads, ADS.P0)

# Establish a serial connection with the Arduino
SER = serial.Serial('/dev/ttyACM0', 9600)

# Define the function that prints the timestamp and the message
class TimestampedPrinter:
    """
    A class that prints a message with a timestamp.
    """
    @staticmethod
    def print_with_timestamp(message):
        """
        Print the message with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d @ %H:%M:%S] ")
        print(f"{timestamp}{message}")


# Define the input sources
def read_gyroscope_state():
    """
    Send the request to the Arduino, then read and convert the response to an integer.
    """
    SER.write(b'get_gyroscope_state\n')
    response = SER.readline().strip().decode()
    return int(response)

RASPBERRY_PI_TEMPERATURE = ADC_0
RASPBERRY_PI_SWITCH = SWITCH_PIN
ARDUINO_UNO_GYROSCOPE = read_gyroscope_state
RASPBERRY_PI_PIR = PIR_PIN

INPUT_SOURCES = [
    RASPBERRY_PI_TEMPERATURE,
    RASPBERRY_PI_SWITCH,
    ARDUINO_UNO_GYROSCOPE,
    RASPBERRY_PI_PIR,
]

# Define the Arduino output functions
def write_buzzer_state(state):
    """
    Send a command to the Arduino to set the buzzer state.
    """
    SER.write(f'buzzer {state}\n'.encode())


def write_led_state(state):
    """
    Send a command to the Arduino to set the LED state.
    """
    SER.write(f'led {state}\n'.encode())


def write_motor_state(state):
    """
    Send a command to the Arduino to set the motor state.
    """
    SER.write(f'motor {state}\n'.encode())


# Define the output destinations
RASPBERRY_PI_RELAY = RELAY_PIN
ARDUINO_UNO_BUZZER = write_buzzer_state
ARDUINO_UNO_LED = write_led_state
ARDUINO_UNO_MOTOR = write_motor_state

OUTPUT_DESTINATIONS = [
    RASPBERRY_PI_RELAY,
    ARDUINO_UNO_BUZZER,
    ARDUINO_UNO_LED,
    ARDUINO_UNO_MOTOR,
]

# Define the conditions and their corresponding inputs and outputs
CONDITIONS = [
    {
        "inputs": [0, 0, 0, 0],
        "outputs": [0, 0, 0, 0]
    },
    {
        "inputs": [0, 0, 0, 1],
        "outputs": [0, 0, 0, 0]
    },
    {
        "inputs": [0, 1, 1, "X"],
        "outputs": [0, 1, 1, 1]
    },
    {
        "inputs": [1, "X", "X", "X"],
        "outputs": [1, 1, 1, 0]
    }
]

# Placeholder for reading input values
def read_inputs():
    # TODO: Replace with actual code to read from physical input sources
    inputs = [0, 0, 0, 0]  # Placeholder for testing
    return inputs

# Placeholder for writing output values
def write_outputs(outputs):
    # TODO: Replace with actual code to write to physical output destinations
    for i, output in enumerate(outputs):
        print(f"Output {i+1} ({OUTPUT_DESTINATIONS[i]}): {output}")

def determine_outputs(inputs):
    for condition in CONDITIONS:
        match = True
        for i, input_value in enumerate(inputs):
            if condition["inputs"][i] != "X" and condition["inputs"][i] != input_value:
                match = False
                break
        if match:
            return condition["outputs"]
    return None

# Main loop to continuously read input values, determine outputs, and write output values
def main():
    while True:
        # Read the input sources
        inputs = read_inputs()
        outputs = determine_outputs(inputs)
        if outputs:
            write_outputs(outputs)
        else:
            print("No matching condition found")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
