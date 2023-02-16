import datetime
import math
import sys
sys.path.insert(0, '/usr/local/lib/python3.9/dist-packages')  # insert the path to the new pyserial package location
import serial
import time
from typing import List , Tuple
import board
import busio
import RPi.GPIO as GPIO
from adafruit_ads1x15 import ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15
###from adafruit_ads1x15 import ads1115 as ADS
###from adafruit_ads1x15.analog_in import AnalogIn


SWITCH_STATE = False
TEMPERATURE_THRESHOLD = 26

# Create the I2C bus
i2c_bus = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c_bus)


# Thinkspeak
WRITE_API_KEY = '87DDHFBW1S25FHVU'
READ_API_KEY = 'I599A9LGA5JIXBBQ'
CHANNEL_ID = '2025339'

# Set the GPIO mode to use BCM numbering
GPIO.setmode(GPIO.BCM)

# GPIO Pin Numbers
PIR_PIN = 18
RELAY_PIN = 22
SWITCH_PIN = 26

# Set up the PIR sensor, the relay and the switch
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create the I2C bus
I2C_BUS = busio.I2C(board.SCL, board.SDA)

'''# Create the ADC object using the I2C bus
ads = ADS.ADS1115(I2C_BUS)
MAX_VOLTAGE = 3.3

# Create single-ended input on channel 0
ADC_0 = AnalogIn(ADS, ADS.P0)'''


# Establish a serial connection with the Arduino
SER = serial.Serial('/dev/ttyUSB0', 9600)

# Define the function that prints the timestamp and the message
import datetime

class TimestampedPrinter:
    """
    A class that provides a utility for printing messages with a timestamp.

    Example usage:
    printer = TimestampedPrinter()
    printer.print_with_timestamp("System initialized.")
    # Output: [2023-02-15 @ 10:30:00] System initialized.
    """
    def print_with_timestamp(self, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d @ %H:%M:%S] ")
        print(f"{timestamp}{message}")
        
tp = TimestampedPrinter()

ads = ADS.ADS1115(i2c_bus)
MAX_VOLTAGE = 3.3

# Create single-ended input on channel 0
ADC_0 = AnalogIn(ads, ADS.P0)

def read_temperature_value() -> None:
    """
    Read the temperature from the ADC and store it in the global variable TEMPERATURE.
    """
    tp.print_with_timestamp("reading temperature value...")
    global TEMPERATURE
    # Read TEMPERATURE and convert to Celsius
    TEMPERATURE = ((ADC_0.voltage / MAX_VOLTAGE) * 10000) / (1 - (ADC_0.voltage / MAX_VOLTAGE))
    TEMPERATURE = 1 / ((1 / 298.15) + (1 / 3950) * math.log(TEMPERATURE / 10000))
    TEMPERATURE = TEMPERATURE - 273.15
    return TEMPERATURE

'''def read_temperature_value() -> None:
    """
    Read the temperature from the ADC and store it in the global variable TEMPERATURE.
    """
    tp.print_with_timestamp("reading temperature value...")
    global TEMPERATURE
    # Read TEMPERATURE and convert to Celsius
    TEMPERATURE = ((ADC_0.voltage / MAX_VOLTAGE) * 10000) / (1 - (ADC_0.voltage / MAX_VOLTAGE))
    TEMPERATURE = 1 / ((1 / 298.15) + (1 / 3950) * math.log(TEMPERATURE / 10000))
    TEMPERATURE = TEMPERATURE - 273.15
    return TEMPERATURE'''



def read_temperature_state() -> int:
    """
    Determine the state of the temperature sensor based on the global variable TEMPERATURE.

    Returns:
        The state of the temperature sensor as an integer:
        - 0: The temperature is below the threshold.
        - 1: The temperature is above or equal to the threshold.
    """
    tp.print_with_timestamp("converting temperature value to state...")
    global TEMPERATURE_STATE
    if TEMPERATURE >= TEMPERATURE_THRESHOLD:
        TEMPERATURE_STATE = 1
    else:
        TEMPERATURE_STATE = 0
    return int(TEMPERATURE_STATE)



def read_switch_state(channel):
    """
    Update SWITCH_STATE when the switch is pressed.

    Args:
        channel: The GPIO channel that the switch is connected to.

    Returns:
        The state of the switch as an integer:
        - 0: The switch is not pressed.
        - 1: The switch is pressed.
    """
    tp.print_with_timestamp("reading switch state...")
    global SWITCH_STATE

    # If SWITCH_STATE is True, set it to False; otherwise, set it to True
    if SWITCH_STATE:
        SWITCH_STATE = False
    else:
        SWITCH_STATE = True

    # Return the current state of the switch as an integer
    return int(SWITCH_STATE)




# Define the input sources
def read_gyro_state() -> int:
    """
    Read the gyroscope state from the Arduino and return it as an integer.

    Returns:
        The gyroscope state as an integer:
        - 0: The gyroscope has not been moved.
        - 1: The gyroscope has been moved.
    """
    tp.print_with_timestamp("reading gyroscope state...")
    # Send a request to the Arduino to get the gyroscope state
    SER.write(b'get_gyroscope_state\n')

    # Read the response from the Arduino and convert it to an integer
    response = SER.readline().strip().decode()
    
    global GYRO_STATE
    try:
        return int(response)
    except ValueError:
        tp.print_with_timestamp(f"Error: Could not convert response '{response}' to an integer")
        return 0
    return int(GYRO_STATE)




def read_pir_state() -> int:
    """
    Read the state of the PIR sensor and return it as an integer.

    Returns:
        The state of the PIR sensor as an integer (0 or 1).
        0 indicates no motion detected, 1 indicates motion detected.
    """
    tp.print_with_timestamp("reading PIR state...")
    global PIR_STATE
    if GPIO.input(PIR_PIN):
        return 1
    else:
        return 0
    return int(PIR_STATE)


# Define the input sources
def read_ALL_inputs() -> List[float]:
    """
    Read input values from various sources and return them as a list.

    Returns:
    
    """
    read_temperature_value()
    read_temperature_state()
    tp.print_with_timestamp("calculating all inputs...")
    global INPUTS
    INPUTS = [TEMPERATURE_STATE, SWITCH_STATE, GYRO_STATE, PIR_STATE]
    return INPUTS

# Placeholder for determining output values
def determine_outputs(inputs: List[float]) -> Tuple[List[int], List[float]]:
    """
    Determine the output values based on the input values and a set of conditions.

    Args:
        inputs: A list of input values.

    Returns:
        A tuple containing a list of output values and a list of input values.
    """
    tp.print_with_timestamp("determining outputs based on inputs calculated...")
    # Define the conditions and their corresponding inputs and outputs
    CONDITIONS = [
        {
            "INPUTS": [0, 0, 0, 0],
            "outputs": [0, 0, 0, 0]
        },
        {
            "INPUTS": [0, 0, 0, 1],
            "outputs": [0, 0, 0, 0]
        },
        {
            "INPUTS": [0, 1, 1, None],
            "outputs": [0, 1, 1, 1]
        },
        {
            "INPUTS": [1, None, None, None],
            "outputs": [1, 1, 1, 0]
        }
    ]

    # Loop through each condition and check if it matches the input values
    for condition in CONDITIONS:
        match = True
        for i, input_value in enumerate(inputs):
            if condition["inputs"][i] is not None and condition["inputs"][i] != input_value:
                match = False
                break
        if match:
            # If the condition matches, return the corresponding outputs and the input values
            return (condition["outputs"], inputs)

    # If none of the conditions match, return a default set of outputs and the input values
    return ([0, 0, 0, 0], INPUTS)

# Define the output functions
def write_buzzer_state(state: int) -> None:
    """
    Send a command to the Arduino to set the buzzer state.

    Args:
        state: The state of the buzzer (0 or 1).
    """
    SER.write(f'buzzer {state}\n'.encode())

def write_led_state(state: int) -> None:
    """
    Send a command to the Arduino to set the LED state.

    Args:
        state: The state of the LED (0 or 1).
    """
    SER.write(f'led {state}\n'.encode())

def write_motor_state(state: int) -> None:
    """
    Send a command to the Arduino to set the motor state.

    Args:
        state: The state of the motor (0 or 1).
    """
    SER.write(f'motor {state}\n'.encode())

def write_relay_state(state: bool) -> None:
    """
    Set the state of the relay.

    Args:
        state: A boolean value indicating whether the relay should be turned on (True) or off (False).
    """
    if state:
        GPIO.output(RELAY_PIN, 1)
    else:
        GPIO.output(RELAY_PIN, 0)

# Placeholder for writing output values
def write_ALL_outputs(outputs: List[int], inputs: List[float]) -> None:
    """
    Write output values to various destinations based on the determine_outputs function.

    Args:
        outputs: A list of output values.
        inputs: A list of input values.
    """
    # Send commands to the Arduino to control the buzzer, LED, and motor
    if outputs[1]:
        write_buzzer_state(True)
    else:
        write_buzzer_state(False)

    if outputs[2]:
        write_led_state(True)
    else:
        write_led_state(False)

    if outputs[3]:
        write_motor_state(True)
    else:
        write_motor_state(False)

    # Set the state of the relay if necessary
    if outputs[0]:
        write_relay_state(True)
    else:
        write_relay_state(False)



# ThinkSpeak Dashboard
def update_and_read_thingspeak(WRITE_API_KEY, READ_API_KEY, CHANNEL_ID):
    tp.print_with_timestamp("initialising thinkspeak...")
    NEXT_WRITE_TIME = time.time()
    NEXT_READ_TIME = time.time()

    while True:
        if time.time() >= NEXT_WRITE_TIME:
            VALUE_INT = 200
            try:
                URL = 'http://api.thingspeak.com/update?api_key=%s&field1=%d' % (WRITE_API_KEY, VALUE_INT)
                F = urllib2.urlopen(URL)
                tp.print_with_timestamp('Updated Thingspeak channel with value: %d' % VALUE_INT)
                F.close()
            except:
                tp.print_with_timestamp('Error updating Thingspeak channel')

            NEXT_WRITE_TIME = time.time() + 20

        if time.time() >= NEXT_READ_TIME:
            try:
                CONN = urllib2.urlopen('http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s' % (CHANNEL_ID, READ_API_KEY))
                RESPONSE = CONN.read()
                DATA = json.loads(RESPONSE)
                tp.print_with_timestamp('Retrieved value from Thingspeak channel: %s' % DATA['field1'])
                CONN.close()
            except:
                tp.print_with_timestamp('Error retrieving value from Thingspeak channel')

            NEXT_READ_TIME = time.time() + 5

        tp.print_with_timestamp('Next Thingspeak update in %d seconds' % int(NEXT_WRITE_TIME - time.time()))
        time.sleep(1)


# Main loop to continuously read input values, determine outputs, and write output values
def main() -> None:
    """
    The main function that continuously reads input values, determines outputs, and writes output values.
    """
    tp.print_with_timestamp("initialising main program...")
    # Register the switch callback function
    GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING, callback=read_switch_state, bouncetime=300)

    while True:
        tp.print_with_timestamp("running main program...")
        # Read the input sources
        inputs = read_ALL_inputs()

        # Determine the output values based on the input values and a set of conditions
        outputs = determine_outputs(inputs)

        # Write the output values to the output destinations
        write_ALL_outputs(outputs, inputs)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
