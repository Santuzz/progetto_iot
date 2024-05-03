import serial
import time
import serial.tools.list_ports
import json
from datetime import datetime
import os
from REST_communication import RestAPI
from django_server.mqtt_integration.MQTT_client import MQTT_client

import sys
try:
    from config import read_serial
except ImportError:
    sys.path.append('..')
    from config import read_serial

# import paho.mqtt.client as mqtt


class Bridge():

    def __init__(self):
        self.serial_port = read_serial()
        # self.setupSerial()
        self.crossroad = "via Bella"
        self.data = {
            "name": self.crossroad,
            "latitude": 46.321,
            "longitude": 11.123,
        }

        self.cars_count = [0, 1, 0, 0]

    def setupSerial(self):
        self.ser = None
        try:
            print("connecting to " + self.serial_port)
            self.ser = serial.Serial(self.serial_port, 9600, timeout=0)
        except serial.SerialException as e:
            print(f"Error in opening the serial port: {e}")
            exit()

    def mqtt_callback(self, message):
        self.msg = message
        print(f'Received message on topic: {self.topic} with payload: {self.msg}')
        # TODO Comunicazione seriale con Arduino
        arduino_data = self.msg

        # Add start and end bytes for data to arduino
        arduino_bytes = [0xFF, arduino_data, 0xFE]
        """try:
                    # self.ser.write(data_bytes)
                    print(f"Sent data: {arduino_bytes}")
                except serial.SerialException as e:
                    print(f"Error sending data: {e}")"""

    def setupMqtt(self):
        self.topic = "data_traffic/" + self.crossroad.lower().replace(" ", "_")
        self.client = MQTT_client("bridge_serial")
        self.client.add_callback(self.mqtt_callback)
        self.client.start(self.topic)
        self.client.subscribe(self.topic)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def loop(self):
        # infinite loop for serial managing

        # current_time = time.time()
        # current_cars = self.cars_count
        self.setupMqtt()
        try:
            while (True):

                # TODO comunicazione MQTT con object_detection/detection_YOLOv8.py
                cars_count = 0

                # ricezione MQTT da server

                time.sleep(1)
        except (KeyboardInterrupt):
            print("Loop interrupted")
            self.client.stop()
            exit(1)


if __name__ == '__main__':
    br = Bridge()
    br.loop()
