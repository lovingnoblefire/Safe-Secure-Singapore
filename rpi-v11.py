''' LIBRARIES & HEADERS '''
import RPi.GPIO as GPIO
import bluetooth
import board
import busio
import datetime
import httplib
import json
import logging
import math
import time
import urllib2
import uuid

from adafruit_ads1x15 import ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


''' RPI CONFIGURATIONS '''
# GPIO Pin Numbers
SWITCH_PIN = 26
RELAY_PIN = 22
PIR_PIN = 18

# Set the GPIO mode to use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up the PIR sensor, the relay and the switch
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Defining Global Variables
SWITCH_STATE = False

# Create the I2C bus
I2C_BUS = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ADS = ADS.ADS1115(I2C_BUS)
MAX_VOLTAGE = 3.3

# Create single-ended input on channels
ADC_0 = AnalogIn(ADS, ADS.P0)



''' USER DEFINED FUNCTIONS '''
# Callback function to be triggered when the switch is pressed
def button_callback(channel):
    global SWITCH_STATE
    SWITCH_STATE = not SWITCH_STATE

# Add event detection to the switch
GPIO.add_event_detect(SWITCH_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Latching Switch function
def toggle_relay(is_on: bool):
    if is_on:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)

# Math for Analog Thermistor resistance to digital DATA
def calculate_temperature():
    # Read TEMPERATURE and convert to Celsius
    TEMPERATURE = ((ADC_0.voltage / MAX_VOLTAGE) * 10000) / (1 - (ADC_0.voltage / MAX_VOLTAGE))
    TEMPERATURE = 1 / ((1 / 298.15) + (1 / 3950) * math.log(TEMPERATURE / 10000))
    TEMPERATURE = TEMPERATURE - 273.15
    return TEMPERATURE

# PIR function
def read_pir():
    return GPIO.input(PIR_PIN)

PIR_STATE = read_pir()


#
''' THINKSPEAK DASHBOARD '''
# Thinkspeak
WRITE_API_KEY = '87DDHFBW1S25FHVU'
READ_API_KEY = 'I599A9LGA5JIXBBQ'
CHANNEL_ID = '2025339'

def update_and_read_thingspeak(WRITE_API_KEY, READ_API_KEY, CHANNEL_ID):
    NEXT_WRITE_TIME = time.time()
    NEXT_READ_TIME = time.time()

    while True:
        if time.time() >= NEXT_WRITE_TIME:
            VALUE_INT = 200
            try:
                URL = 'http://api.thingspeak.com/update?api_key=%s&field1=%d' % (WRITE_API_KEY, VALUE_INT)
                F = urllib2.urlopen(URL)
                print('Updated Thingspeak channel with value: %d' % VALUE_INT)
                F.close()
            except:
                print('Error updating Thingspeak channel')

            NEXT_WRITE_TIME = time.time() + 20

        if time.time() >= NEXT_READ_TIME:
            try:
                CONN = urllib2.urlopen('http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s' % (CHANNEL_ID, READ_API_KEY))
                RESPONSE = CONN.read()
                DATA = json.loads(RESPONSE)
                print('Retrieved value from Thingspeak channel: %s' % DATA['field1'])
                CONN.close()
            except:
                print('Error retrieving value from Thingspeak channel')

            NEXT_READ_TIME = time.time() + 5

        print('Next Thingspeak update in %d seconds' % int(NEXT_WRITE_TIME - time.time()))
        time.sleep(1)

# Print functions
def display_status(TEMPERATURE, SWITCH_STATE, PIR_STATE):
    CURRENT_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(F"{CURRENT_TIME}")
    print(F"Temperature: {TEMPERATURE}")
    print(F"Switch State: {SWITCH_STATE}")
    print(F"PIR State: {PIR_STATE}")



''' FUNCTIONS TO HANDLE CONDITIONS '''
# Perform action for condition 0
def handle_condition_0():
    print("Handling Condition 0")
    display_status(CALCULATE_TEMPERATURE, SWITCH_STATE, PIR_STATE)
    

def handle_condition_1():
    # Perform action for condition 1
    print("Handling condition 1")

def handle_condition_2():
    # Perform action for condition 2
    print("Handling condition 2")

def handle_condition_3():
    # Perform action for condition 3
    print("Handling condition 3")


def main():
    while True:
        update_and_read_arduino()
        CURRENT_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(F"{CURRENT_TIME}: Initialising Main Program")
        time.sleep(1)
        print(F"{CURRENT_TIME}: Successfully Initialised. Starting Main Program now.")


        # Get the current TEMPERATURE
        TEMPERATURE = calculate_temperature()
        # Get the current PIR state
        PIR_STATE = read_pir()
        # Display the states
        display_status(TEMPERATURE, SWITCH_STATE, PIR_STATE)
        # Publish the states
        publish_states(TEMPERATURE, SWITCH_STATE, PIR_STATE)

        update_and_read_thingspeak(WRITE_API_KEY, READ_API_KEY, CHANNEL_ID)
        
        # Handle conditions
        if SWITCH_STATE:
            if PIR_STATE:
                handle_condition_1()
            else:
                handle_condition_2()
        else:
            if PIR_STATE:
                handle_condition_3()
            else:
                handle_condition_0()
        # Wait for 5 seconds
        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()