import configparser


def read_serial():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        serial_port = config['DEFAULT']['SERIAL_PORT']
        return serial_port
    except KeyError as e:
        print(f"Chiave mancante nel file di configurazione: {e}")
        exit(1)
    except Exception as e:
        print(f"Errore nel caricamento del file di configurazione: {e}")
        exit(1)


def read_network():
    config = configparser.ConfigParser()
    try:
        config.read('../config.ini')
        # server_address = config.get("DEFAULT", "SERVER_ADDRESS")
        server_address = config['DEFAULT']['SERVER_ADDRESS']
        return server_address
    except KeyError as e:
        print(f"Chiave mancante nel file di configurazione: {e}")
        exit(1)
    except Exception as e:
        print(f"Errore nel caricamento del file di configurazione: {e}")
        exit(1)
