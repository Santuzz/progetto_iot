import paho.mqtt.client as mqtt  # import the client1
import json
from datetime import datetime


class MQTTClient:
    def __init__(self, broker_address="localhost", broker_port=1883):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.message_payload = None  # attribute to store the message payload
        self.timestamp_message = None  # attribute to store the timestamp of the message

    def on_connect(self, client, userdata, flags, rc, *args, **kwargs):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed with code", rc)

    def on_disconnect(self, client, userdata, rc, *args, **kwargs):
        print("Disconnected from broker")

    def on_message(self, client, userdata, message):
        print("Received message:", str(message.payload.decode("utf-8")))
        self.message_payload = json.loads(message.payload)  # save the message in the payload
        # print("msg_payload:", self.message_payload)
        self.timestamp_message = datetime.now()
        print("Timestamp message:", self.timestamp_message)

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def disconnect(self):
        self.client.on_disconnect = self.on_disconnect
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, topic):
        print("Subscribing to topic " + topic)
        self.client.subscribe(topic)

    def publish(self, topic, data):
        print("Publishing message to topic " + topic)
        json_data = json.dumps(data)
        self.client.publish(topic, json_data)
        print("Message published:" + str(data))

    def message(self):
        self.client.on_message = self.on_message

    def get_message_payload(self):
        # print("msg_payload:", self.message_payload)
        return self.message_payload

    def message_None(self):
        self.message_payload = None

    # TODO dovrebbe essere inutile
    def get_timestamp_message(self):
        print("timestamp_message:", self.timestamp_message)
        return self.timestamp_message
