import serial
import time
import serial.tools.list_ports
import numpy as np
from datetime import datetime, timedelta
from REST_communication import RestAPI
from django_server.mqtt_integration.MQTT_client import MQTT_client

import sys
try:
    from config import read_serial
    from object_detection.mqtt_client import MQTTClient
except ImportError:
    sys.path.append('..')
    from config import read_serial
    from object_detection.mqtt_client import MQTTClient

# import paho.mqtt.client as mqtt


class Bridge():

    def __init__(self):
        self.crossroad = "incrocio Bellissimo"
        self.data = {
            "name": self.crossroad,
            "latitude": 46.321,
            "longitude": 11.123,
        }

        self.cars_count = [0, 1, 0, 0]
        self.server_connection = True
        self.setupSerial()
        self.setupMqttServer()
        self.setupMqttGateway()
        self.last_server = time.time()*1000-31000
        self.msg = 0

    def setupSerial(self):
        # serial_port = 'COM3'
        serial_port = '/dev/cu.usbmodem1301'
        serial_baudrate = 9600
        try:
            self.ser = serial.Serial(serial_port, serial_baudrate)
            print(f"Serial connection opened on port {serial_port}")
        except serial.SerialException as e:
            print(f"Error in opening the serial port: {e}")
            exit()

    def mqtt_callback(self, message):
        self.msg = int(message)
        self.last_server = time.time()*1000
        print(f'Received message on topic: {self.topic} with payload: {self.msg}')

    def setupMqttServer(self):
        self.topic = "data_traffic/" + self.crossroad.lower().replace(" ", "_")
        self.client_s = MQTT_client("bridge_serial")
        self.client_s.add_callback(self.mqtt_callback)
        self.client_s.start(self.topic)
        self.client_s.subscribe(self.topic)

    def setupMqttGateway(self):
        self.client_g = MQTTClient()  # create new instance of camera
        self.client_g.message()
        self.client_g.connect()
        print('\n')
        self.client_g.subscribe("data_camera")
        print('\n')

    def serialSend(self, plus_time):
        self.ser.write(b'\xFF')
        self.ser.write(int.to_bytes(plus_time, length=1, byteorder='little'))
        self.ser.write(b'\xFE')

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def loop(self):
        t = datetime.now()
        previous_time = t - timedelta(seconds=5)
        plus_time = 0

        try:
            while (True):

                timestamp_message = self.client_g.get_timestamp_message()
                print("Received timestamp_message_bridge:", timestamp_message)

                current_time = datetime.now()
                time_difference = current_time - previous_time
                print("time_difference:", time_difference)
                five_seconds = timedelta(seconds=5)
                if time_difference >= five_seconds:
                    if self.client_g.get_message_payload() is not None:
                        now = time.time()*1000
                        # se sono passati 30 secondi dall'ultima ricezione MQTT del server
                        # allora si guarda il valore inviato dal gateway
                        if now-self.last_server > 30000:
                            message_payload = self.client_g.get_message_payload()
                            print("Received message_payload_bridge:", message_payload)

                            message_camera = np.array(message_payload)

                            self.client_g.message_None()

                            road_a = message_camera[0] + message_camera[2]
                            road_b = message_camera[1] + message_camera[3]
                            print("road_a:", road_a)
                            print("road_b:", road_b)

                            if (road_a > road_b):
                                plus_time = 10 * int(road_a)
                            elif (road_a == road_b):
                                plus_time = 0
                            else:
                                plus_time = -2 * int(road_b)

                            print("plus_time", plus_time)
                            print('\n')
                            self.serialSend(plus_time)
                            previous_time = timestamp_message
                    else:
                        if plus_time != self.msg:
                            self.serialSend(self.msg)
                            plus_time = self.msg

                else:
                    print("Less than 5 seconds have passed since the message arrival compared to the current time.")
                    print('\n')
                    self.client_g.message_None()

                time.sleep(1)
        except (KeyboardInterrupt):
            print("Loop interrupted")
            self.client_g.stop()
            self.client_s.disconnect()
            print("Serial disconnected")
            self.ser.close()
            exit(1)


if __name__ == '__main__':
    br = Bridge()
    br.loop()
