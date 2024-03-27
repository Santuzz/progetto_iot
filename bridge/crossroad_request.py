from bridge.REST_communication import RestAPI
import requests
import sys

ip_address = "localhost"


def main():
    master = RestAPI(user={'email': 'admin@admin.com', 'password': 'admin',
                     'username': 'admin'}, base_url="http://"+ip_address+":8000/api/")
    data = {
        "name": "Giorgio",

    }
    master.create_instance("crossroad", data)


if __name__ == "__main__":
    main()
