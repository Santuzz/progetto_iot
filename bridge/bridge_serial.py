import serial
import time
import serial.tools.list_ports

import configparser

import json
from datetime import datetime
import os
from REST_communication import RestAPI
# import paho.mqtt.client as mqtt


def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        server_address = config.get("DEFAULT", "SERVER_ADDRESS")
        serial_port = config['DEFAULT']['SERIAL_PORT']
        return server_address, serial_port
    except KeyError as e:
        print(f"Chiave mancante nel file di configurazione: {e}")
        exit(1)
    except Exception as e:
        print(f"Errore nel caricamento del file di configurazione: {e}")
        exit(1)


class Bridge():

    def __init__(self):
        self.base_url, self.serial_port = read_config()
        # self.setupSerial()
        self.crossroad = "viaBella"
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

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def setupServer(self, rest):
        # get existed crossroad
        return rest.get_instance("crossroad", self.crossroad)
        # create crossroad
        return rest.create_instance("crossroad", self.data)

    def loop(self):
        # infinite loop for serial managing
        rest = RestAPI(user={'email': 'admin@admin.com', 'password': 'admin', 'username': 'admin'})
        self.setupServer(rest)
        current_time = time.time()
        current_cars = self.cars_count
        while (True):
            # TODO Controllare se manda correttamente i dati
            # Your data to send
            # Replace with your actual data (integer in this example)
            data_to_send = 42

            # Send data with start and end bytes
            data_bytes = [0xFF, data_to_send, 0xFE]  # List of bytes to send
            try:
                # self.ser.write(data_bytes)
                print(f"Sent data: {data_bytes}")
            except serial.SerialException as e:
                print(f"Error sending data: {e}")

            # TODO parte per leggere da MQTT
            cars_count = 0

            # TODO parte per comunicare con il server attraverso API

            if time.time()-current_time >= 5:
                if current_cars != self.cars_count:
                    rest.send_count(self.crossroad, self.cars_count)
                    current_cars = self.cars_count
                    self.cars_count = [1, 0, 0, 0]

                # codice di test
                else:
                    self.cars_count = [1, 0, 0]

                current_time = time.time()

            # Wait for a bit before sending again (adjust as needed)
            time.sleep(1)  # Wait 1 second before sending again


if __name__ == '__main__':
    br = Bridge()
    br.loop()
