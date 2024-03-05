import serial

# Configurazione della porta seriale per Arduino
serial_port = 'COM4'  # Assicurati che corrisponda alla porta seriale a cui è collegato Arduino
serial_baudrate = 9600


# Funzione per inviare dati ad Arduino tramite la comunicazione seriale
def send_to_arduino(data):
    try:
        # Apri la connessione seriale con Arduino
        ser = serial.Serial(serial_port, serial_baudrate)
        print(f"Connessione seriale aperta su porta {serial_port}")

        # Invia i dati ad Arduino
        ser.write(data.encode())
        print(f"Dati inviati ad Arduino: {data}")

        # Chiudi la connessione seriale
        ser.close()
        print("Connessione seriale chiusa")
    except serial.SerialException as e:
        print(f"Errore durante l'apertura della connessione seriale: {e}")


# Chiamata alla funzione per inviare dati ad Arduino
message_camera = [1,2,3,4]
send_to_arduino(message_camera)
