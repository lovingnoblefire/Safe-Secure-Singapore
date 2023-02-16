import serial
import datetime
import time

# Define the function that prints the timestamp and the message
class TimestampedPrinter:
    def __init__(self):
        pass

    def print_with_timestamp(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d @ %H:%M:%S] ")
        print(f"{timestamp}{message}")

# Define the constants for the condition handlers
CONDITION_0 = b'CONDITION_0'
CONDITION_1 = b'CONDITION_1'
CONDITION_2 = b'CONDITION_2'
CONDITION_3 = b'CONDITION_3'

# Define the condition handlers
def handle_condition_0(tp):
    tp.print_with_timestamp("Condition 0 detected, performing action...")
    # TODO: insert code to turn off the relay connected to the door lock here
    # TODO: insert code to turn off the buzzer here
    # TODO: insert code to turn off the LED here
    # TODO: insert code to stop the motor connected to the door handle here
    tp.print_with_timestamp("End of Condition 0")

def handle_condition_1(tp):
    tp.print_with_timestamp("Condition 1 detected, performing action...")
    # TODO: insert code to turn on the relay connected to the door lock here
    # TODO: insert code to turn off the buzzer here
    # TODO: insert code to turn off the LED here
    # TODO: insert code to stop the motor connected to the door handle here
    tp.print_with_timestamp("End of Condition 1")

def handle_condition_2(tp):
    tp.print_with_timestamp("Condition 2 detected, performing action...")
    # TODO: insert code to turn on the LED here
    # TODO: insert code to start the motor connected to the door handle here
    # TODO: insert code to turn off the relay connected to the door lock here
    # TODO: insert code to turn off the buzzer here
    tp.print_with_timestamp("End of Condition 2")

def handle_condition_3(tp):
    tp.print_with_timestamp("Condition 3 detected, performing action...")
    # TODO: insert code to turn off the relay connected to the door lock here
    # TODO: insert code to turn on the buzzer here
    # TODO: insert code to turn on the LED here
    # TODO: insert code to stop the motor connected to the door handle here
    tp.print_with_timestamp("End of Condition 3")


# Open a serial connection to the Arduino at 9600 baud
ser = serial.Serial('/dev/ttyACM0', 9600)

# Create an instance of the TimestampedPrinter class
tp = TimestampedPrinter()

# Main loop
while True:
    # Wait for incoming data from the Arduino
    if ser.in_waiting > 0:
        data = ser.readline().strip()

        # Split the data into command and argument
        parts = data.split(b':')
        command = parts[0]
        argument = parts[1] if len(parts) > 1 else b''

        # Call the appropriate condition handler based on the command
        if command == CONDITION_0:
            handle_CONDITION_0(tp)
        elif command == CONDITION_1:
            handle_CONDITION_1(tp)
        elif command == CONDITION_2:
            handle_CONDITION_2(tp)
        elif command == CONDITION_3:
            handle_CONDITION_3(tp)
        else:
            tp.print_with_timestamp(f"Invalid command: {command.decode()}")

    # Check if the door handle has been moved
    # TODO: implement the code for checking if the door handle has been moved using the gyroscope

    # If the door handle has been moved, send a signal to the Raspberry Pi
    # TODO: implement the code for sending a signal to the Raspberry Pi if the door handle has been moved

    # Wait for some time before checking the door handle again
    sleep(0.1)
