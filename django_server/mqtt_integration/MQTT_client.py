import paho.mqtt.client as mqtt
from django.conf import settings

import sys
try:
    from config import read_mqtt
except ImportError:
    sys.path.append('..')
    from config import read_mqtt


class MQTT_client():

    def __init__(self, id):
        config = read_mqtt()
        self.client_id = id
        self.broker_ip = config['broker_host']
        self.broker_port = config['broker_port']
        self.qos = config['qos']
        self.keep_alive = config['broker_keepalive']
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.client_id)
        # self.client.username_pw_set(username=settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.on_publish = self.on_publish
        # self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f'MQTT: client {self.client_id} connected succesfully at {self.broker_ip}:{self.broker_port}')
        else:
            print("Connection failed with code", rc)
        self.client.subscribe(self.topic, qos=self.qos)

    def on_disconnect(self, client, userdata, rc, *args, **kwargs):
        print("MQTT client disconnected")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode('utf-8')
        # print(f'Client: {self.client_id} received message on topic: {msg.topic} with payload: {message}')

        if hasattr(self, 'callback'):
            self.callback(message)

    def add_callback(self, callback):
        self.callback = callback

    """def on_publish(self, client, userdata, mid):
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        pass
"""

    def publish(self, message):
        self.client.publish(self.topic, message, qos=self.qos, retain=False)

    def subscribe(self, topic):
        print("Subscribing to topic " + topic)
        self.client.subscribe(topic)

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def start(self, topic):
        self.topic = topic  # Inizializza il topic prima di connetterti
        print(f'MQTT client {self.client_id} connecting to {self.broker_ip}:{self.broker_port}')
        self.client.connect(self.broker_ip, self.broker_port, self.keep_alive)
        self.client.loop_start()
