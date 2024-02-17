import serial
import serial.tools.list_ports

import configparser

import json
from datetime import datetime
import os
# import paho.mqtt.client as mqtt


class Bridge():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.setupSerial()

    def setupSerial(self):
        # open serial port
        self.ser = None
        self.portname = None

        if self.config.get("Serial", "UseDescription", fallback=False):
            self.portname = self.config.get(
                "Serial", "PortName", fallback="COM1")
        else:
            print("list of available ports: ")
            ports = serial.tools.list_ports.comports()

            for port in ports:
                print(port.device)
                print(port.description)
                # if self.config.get("Serial", "PortDescription", fallback="arduino").lower() \
                #         in port.description.lower():
                #    self.portname = port.device
                if "/dev/cu.usbmodem11101" in port.device:
                    self.portname = port.device
                    break  # Esci dal ciclo una volta trovata la corrispondenza

        try:
            if self.portname is not None:
                print("connecting to " + self.portname)
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None

        # self.ser.open()

        # internal input buffer from serial
        self.inbuffer = []

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def loop(self):
        # infinite loop for serial managing
        #
        while (True):
            # look for a byte from serial
            if not self.ser is None:

                if self.ser.in_waiting > 0:
                    # data available from the serial port
                    lastchar = self.ser.read(1)

                    if lastchar == b'\xfe':  # EOL
                        print("\nValue received")
                        self.useData()
                        self.inbuffer = []
                    else:
                        # append
                        self.inbuffer.append(lastchar)

    def useData(self):
        # I have received a packet from the serial port. I can use it
        if len(self.inbuffer) < 3:   # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        numval = int.from_bytes(self.inbuffer[1], byteorder='little')

        sensor_name = "variable resistor"
        sensor_data = {
            "name": sensor_name,
            "data": []
        }

        for i in range(numval):
            val = int.from_bytes(self.inbuffer[i+2], byteorder='little')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            sensor_data["data"].append({
                "value": val,
                "timestamp": timestamp
            })
         # Determine the path to data.json relative to the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', 'flask_server', 'data.json')

        # Read existing data from data.json
        try:
            with open(json_path, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {"sensors": []}

        # Update or add sensor data
        sensor_found = False
        for existing_sensor in existing_data["sensors"]:
            if existing_sensor["name"] == sensor_name:
                existing_sensor["data"].extend(sensor_data["data"])
                sensor_found = True
                break

        if not sensor_found:
            existing_data["sensors"].append(sensor_data)

        # Write the updated data back to data.json, overwriting the existing file
        with open(json_path, 'w') as file:
            json.dump(existing_data, file, indent=2)

        # Print the added values for testing
        for data_entry in sensor_data["data"]:
            strval = f"{sensor_name}: {data_entry['value']} at {data_entry['timestamp']}"
            print(strval)

        return True


if __name__ == '__main__':
    br = Bridge()
    br.loop()
