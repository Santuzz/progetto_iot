import paho.mqtt.client as mqtt
from django.conf import settings


class MQTT_client:

    def __init__(self, topic):
        self.client_id = settings.MQTT_CLIENT_ID
        self.broker_ip = settings.MQTT_BROKER_HOST
        self.broker_port = settings.MQTT_BROKER_PORT
        self.qos = settings.MQTT_QOS
        self.topic = topic
        self.keep_alive = settings.MQTT_BROKER_KEEPALIVE
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=self.client_id)
        self.client.username_pw_set(username=settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f'MQTT: client {self.client_id} connected succesfully at {self.broker_ip}:{self.broker_port}')
        self.client.subscribe(self.topic, qos=self.qos)
        # self.client.will_set('bug', payload='offline', qos=self.qos, retain=True)

    def on_message(self, client, userdata, msg):  # Prova di fuzionamento, DA CAMBIARE TODO
        print(f'Client: {self.client_id} received message on topic: {msg.topic} with payload: {msg.payload}')

    def on_publish(self, client, userdata, mid):
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        pass

    def on_disconnect(self, client, userdata, rc, properties=None):
        print("MQTT client disconnected")

    def publish(self, message):
        self.client.publish(self.topic, message, qos=self.qos, retain=False)

    def disconnect(self):
        self.client.disconnect()

    def stop(self):
        self.client.loop_stop()

    def start(self):
        print(f'MQTT client {self.client_id} connecting to {self.broker_ip}:{self.broker_port}')
        self.client.connect(self.broker_ip, self.broker_port, self.keep_alive)
        self.client.loop_start()
