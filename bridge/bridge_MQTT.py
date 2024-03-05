import serial
import paho.mqtt.client as mqtt

# Configurazione del broker MQTT
mqtt_broker_host = "localhost"  # Indirizzo del broker MQTT
mqtt_topic = "arduino/data"  # Topic MQTT da cui leggere i dati

# Configurazione della porta seriale per Arduino
serial_port = 'COM4'  # Specificare la porta seriale corretta per Arduino
serial_baudrate = 9600


# Funzione di callback chiamata alla connessione al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connesso al broker MQTT con codice di ritorno: " + str(rc))
    client.subscribe(mqtt_topic)  # Iscrizione al topic MQTT


# Funzione di callback chiamata alla ricezione di un messaggio MQTT
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Messaggio ricevuto dal broker MQTT: " + message)
    send_to_arduino(message)


# Funzione per inviare dati ad Arduino tramite la comunicazione seriale
def send_to_arduino(data):
    ser.write(data.encode())  # Invio dei dati ad Arduino

# Inizializzazione della connessione seriale con Arduino
ser = serial.Serial(serial_port, serial_baudrate)

# Inizializzazione del client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connessione al broker MQTT
client.connect(mqtt_broker_host, 1883, 60)

# Avvio del loop per la gestione dei messaggi MQTT
client.loop_forever()
