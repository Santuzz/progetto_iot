import requests
import sys
from ..bridge.REST_comunication import RestAPI

ip_address = "localhost"


def main():
    master = RestAPI(user={'email': 'admin@admin.com', 'password': 'admin',
                     'username': 'admin'}, base_url="http://"+ip_address+":8000/api/")
