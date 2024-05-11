import serial
import numpy as np
from datetime import datetime
from datetime import timedelta
import time
#import struct

import sys
try:
    from object_detection.mqtt_client import MQTTClient
except ImportError:
    sys.path.append('..')
    from object_detection.mqtt_client import MQTTClient

# Configuration of the serial port for Arduino
serial_port = 'COM3'  # Correct serial port for Arduino
serial_baudrate = 9600

# Open serial connection with Arduino
ser = serial.Serial(serial_port, serial_baudrate)
print(f"Serial connection opened on port {serial_port}")

client = MQTTClient()  # create new instance of camera
client.message()
client.connect()
print('\n')
client.subscribe("data_camera")
print('\n')

def serialSend(plus_time):
    # Send start byte to Arduino
    ser.write(b'\xFF')
    # Send data to Arduino
    #byte_data = struct.pack('i', plus_time)
    #ser.write(plus_time & 0xFF)
    #ser.write((plus_time >> 8) & 0xFF)
    ser.write(int.to_bytes(plus_time, length=1, byteorder='little'))
    #print(f"Data sent to Arduino: {byte_data}")
    # Send end byte to Arduino
    ser.write(b'\xFE')

# Wait until a new message is received
#while client.get_message_payload() is None:
 #   pass

t = datetime.now()
previous_time = t - timedelta(seconds=5)
#print("previous_time:", previous_time)
#print('\n')

try:
    while (True):

    # Wait until a new message is received
        while client.get_message_payload() is None:
            pass

        # while client.get_timestamp_message() is None:
        #    pass

        # Get the arrival time of the message from the MQTT client
        timestamp_message = client.get_timestamp_message()
        print("Received timestamp_message_bridge:", timestamp_message)

        current_time = datetime.now()
        #print("current_time:", current_time)

        # Determine the time difference
        time_difference = current_time - previous_time
        print("time_difference:", time_difference)

        # Create a timedelta object to represent 5 seconds
        five_seconds = timedelta(seconds=5)
        #print("five_seconds", five_seconds)

        # Compare the time difference with 5 seconds
        if time_difference >= five_seconds:
            # Get the message from the MQTT client
            message_payload = client.get_message_payload()
            print("Received message_payload_bridge:", message_payload)

            message_camera = np.array(message_payload)
            #print("message_camera:", message_camera)
            #print('\n')

            client.message_None()

            road_a = message_camera[0] + message_camera[2]
            road_b = message_camera[1] + message_camera[3]
            print("road_a:", road_a)
            print("road_b:", road_b)
            plus_time = 0

            if (road_a > road_b):
                plus_time = 2 * int(road_a)
            elif (road_a == road_b):
                plus_time = 0
            else:
                plus_time = -2 * int(road_b)

            print("plus_time", plus_time)
            print('\n')

            serialSend(plus_time)
            #byte_send = ser.read(2)
            #print("Message received by Arduino:", ser.readline())

            previous_time = timestamp_message
            #print("previous_time:", previous_time)
            #print('\n')
        else:
            print("Less than 5 seconds have passed since the message arrival compared to the current time.")
            print('\n')
            client.message_None()

except (KeyboardInterrupt):
        print()
        print("Loop interrupted")
        client.disconnect()
        print("Serial disconnected")
        ser.close()
        exit(1)
