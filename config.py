import configparser


def read_serial():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        serial_port = config['DEFAULT']['SERIAL_PORT']
        return serial_port
    except KeyError as e:
        print(f"Missing key: {e}")
        exit(1)
    except Exception as e:
        print(f"Error during config file loading: {e}")
        exit(1)


def read_network():
    config = configparser.ConfigParser()
    try:
        config.read('../config.ini')
        # server_address = config.get("DEFAULT", "SERVER_ADDRESS")
        server_address = config['DEFAULT']['SERVER_ADDRESS']
        return server_address
    except KeyError as e:
        print(f"Missing key: {e}")
        exit(1)
    except Exception as e:
        print(f"Error during config file loading: {e}")
        exit(1)


def read_increment():
    config = configparser.ConfigParser()
    try:
        config.read('../config.ini')
        increment = config['DJANGO']['INCREMENT_PER_CAR']
        return int(increment)
    except KeyError as e:
        print(f"Missing key: {e}")
        exit(1)
    except Exception as e:
        print(f"Error during config file loading: {e}")
        exit(1)


def read_mqtt():
    config = configparser.ConfigParser()
    try:
        config.read('../config.ini')
        parameters = config['MQTT']
        return parameters
    except KeyError as e:
        print(f"Missing key: {e}")
        exit(1)
    except Exception as e:
        print(f"Error during config file loading: {e}")
        exit(1)
