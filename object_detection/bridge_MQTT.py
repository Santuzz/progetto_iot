import serial
import json
from mqtt_client import MQTTClient
import numpy as np

# Configuration of the serial port for Arduino
serial_port = 'COM4'  # Correct serial port for Arduino
serial_baudrate = 9600

client = MQTTClient()          #create new instance of camera
client.message()
client.connect()
print('\n')
client.subscribe("data_camera")
print('\n')


# Function to send data to Arduino via serial communication
def send_to_arduino(data):
    try:
        # Open serial connection with Arduino
        ser = serial.Serial(serial_port, serial_baudrate)
        print(f"Serial connection opened on port {serial_port}")

        # Send data to Arduino
        ser.write(data.encode())
        print(f"Data sent to Arduino: {data}")

        # Close serial connection
        ser.close()
        print("Serial connection closed")
    except serial.SerialException as e:
        print(f"Error opening serial connection: {e}")

# Wait until a new message is received
while client.get_message_payload() is None:
    pass

# Get the message from the MQTT client
message_payload = client.get_message_payload()
print("Received message_payload_bridge:", message_payload)

message_camera = np.array(message_payload)


# Chiamata alla funzione per inviare dati ad Arduino
# send_to_arduino(json.dumps(message_payload))
print('\n')
client.disconnect()
