import serial
import json
from mqtt_client import MQTTClient
import numpy as np
from datetime import datetime
from datetime import timedelta
import time
import struct

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
# TODO questo si può togliere, no?
#while client.get_message_payload() is None:
 #   pass

# TODO al posto di datetime.now() che ritorna anche la data, si potrebbe optare per time.time()che restituisce direttamenti i secondi
t = datetime.now()
previous_time = t - timedelta(seconds=5)
#print("previous_time:", previous_time)
#print('\n')

try:
    while (True):

    # Wait until a new message is received
    # TODO rimuovere questo loop perchè altrimenti il bridge rimane bloccato a far nulla
    # oltre a captare i messaggi sul topic MQTT deve anche comunicare con arduino e con il server
    # da sostituire con un if visto che siamo già in un ciclo infinito
        while client.get_message_payload() is None:
            pass

        # while client.get_timestamp_message() is None:
        #    pass

        # Get the arrival time of the message from the MQTT client
        # TODO da rimuovere perchè il tempo lo calcoliamo direttamente con la funzione time.time()
        timestamp_message = client.get_timestamp_message()
        print("Received timestamp_message_bridge:", timestamp_message)

        current_time = datetime.now()
        #print("current_time:", current_time)

        # Determine the time difference
        time_difference = current_time - previous_time
        print("time_difference:", time_difference)

        # Create a timedelta object to represent 5 seconds
        # TODO se non si usa datetime questa variabile risulta inutile
        five_seconds = timedelta(seconds=5)
        #print("five_seconds", five_seconds)

        # Compare the time difference with 5 seconds
        # TODO la condizione potrebbe essere: time.time() - previous_time >= 5
        # e alla fine dell'if si aggiorna previous_time con time.time()
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
        exit(1)
