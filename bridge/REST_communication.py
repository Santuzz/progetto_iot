import requests
import datetime
import argparse
import sys
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
import time

try:
    from config import read_network
except ImportError:
    sys.path.append('..')

    from config import read_network


class RestAPI:
    def __init__(self, user):
        self.base_url = read_network()
        self.user = user
        if user.get('password') is None or (user.get('username') is None and user.get('email') is None):
            raise Exception(
                'Errore: Password and at least one of username and email must be provided')
        self.token = self.get_auth_token()

    def get_auth_token(self):
        token_url = self.base_url + 'token/'
        retry_count = 0
        max_retries = 1

        while retry_count < max_retries:
            try:
                response = requests.get(token_url, data={
                    'password': self.user.get('password'),
                    'email': self.user.get('email'),  # Assuming 'email' is the correct field rather than 'username'
                    'username': self.user.get('username')
                })
                response.raise_for_status()  # This will raise an HTTPError for bad responses (4XX or 5XX)

                # If response is successful, extract token and return
                token_data = response.json()
                if 'token' in token_data:
                    return token_data['token']
                else:
                    print("Token not found in response. Here is the response data for debugging:")
                    print(token_data)
                    break

            except (ConnectionError, Timeout) as e:
                print(f"Network error: {e}. Retrying... ({retry_count + 1}/{max_retries})")
                retry_count += 1
                time.sleep(1)  # Wait for 2 seconds before retrying

            except HTTPError as e:
                print(f"HTTP error: {e}. Response status code: {response.status_code}")
                print(response.text)
                break

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        print("Failed to obtain the token after maximum retries.")
        return None

    def get_current_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def request(self, method, url, data=None):
        headers = {'Content-type': 'application/json',
                   'Authorization': f'Token {self.token}'}
        response = requests.request(
            method, self.base_url + url, json=data, headers=headers)
        return response

    def create_instance(self, model_name, data):
        url = f'{model_name.lower()}/'
        response = self.request("POST", url, data)
        print(response.json())
        return response

    def delete_instance(self, model_name, id):
        url = f'{model_name.lower()}/{id}/'
        response = self.request('DELETE', url)
        try:
            print(response.json())
        except:
            pass
        return response

    def update_instance(self, model_name, id, data):
        url = f'{model_name.lower()}/{id}/'
        response = self.request('PUT', url, data)
        print(response.json())
        return response

    def get_instance(self, model_name, id=None):
        if id is None:
            url = f'{model_name.lower()}/'
        else:
            url = f'{model_name.lower()}/{id}/'
        response = self.request('GET', url)
        return response

    def send_count(self, crossroad, cars_count):
        url = f'crossroad/'
        crossroad = crossroad.lower()
        # convert from list to string
        cars_count = ", ".join(str(num) for num in cars_count)
        last_send = self.get_current_date()
        data = {"cars_count": cars_count,
                "last_send": last_send,
                "name": crossroad}
        response = self.request('PUT', url+crossroad+"/", data)
        return response


def fill_data(args):
    data = {
        'id': None,
        'cars_count': None,
        'crossroad_name': None,
        'active': None,
        'name': None,
        'latitude': None,
        'longitude': None,
        'traffic_level': None,
        'street': None,
        'length': None,
        'alert': None,
        'direction': None,
        'green_value': None,
        'street_name': None
    }
    if args.model == 'webcam':
        if args.id is not None:
            data['id'] = args.id
        if args.crossroad is not None:
            data['crossroad_name'] = args.crossroad
        if args.active.lower() == "true":
            data['active'] = True
        elif args.active.lower() == "false":
            data['active'] = False

        elif args.crossroad is None:
            print(
                "Error: provide at least --crossroad, --id or --active for a webcam")
            exit(1)

    elif args.model == 'crossroad':
        if args.name is not None:
            data['name'] = args.name
        else:
            print("Error: Argument --name must be provided for a crossroad")
            exit(1)
        if args.active:
            if args.active.lower() == "true":
                data['active'] = True
            elif args.active.lower() == "false":
                data['active'] = False
        if args.lat is not None:
            data['latitude'] = args.lat
        if args.lon is not None:
            data['longitude'] = args.lon
        if args.traffic is not None:
            data['traffic_level'] = args.traffic
        if args.cars is not None:
            data['cars_count'] = args.cars

    elif args.model == 'street':
        if args.name is not None:
            data['name'] = args.name
        else:
            print("Error: Argument --name must be provided for a street")
            exit(1)
        if args.crossroad is not None:
            data['crossroad_name'] = args.crossroad
        if args.length is not None:
            data['length'] = args.length
        if args.alert is not None:
            data['alert'] = args.alert

    elif args.model == 'trafficlight':
        if args.id is not None:
            data['id'] = args.id
        if args.crossroad is not None:
            data['crossroad_name'] = args.crossroad
        if args.direction is not None:
            data['direction'] = args.direction
        if args.green is not None:
            data['green'] = args.green
        if args.street is not None:
            data['street'] = args.street
        elif args.crossroad is None and args.direction is None and args.green is None:
            print(
                "Error: provide at least --crossroad, --direction, --green, --id or --street for a trafficlight")
            exit(1)
    data = {k: v for k, v in data.items() if v is not None}
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--username', type=str, required=False,
                        help='Username for authentication')
    parser.add_argument('--password', type=str, required=False,
                        help='Password for authentication')
    parser.add_argument('--email', type=str, required=False,
                        help='Email for authentication')

    parser.add_argument(
        '--model', choices=['webcam', 'crossroad', 'street', 'trafficlight'], required=True, help='Select model')
    parser.add_argument(
        '--method', choices=['GET', 'POST', 'PUT', 'DELETE'], required=True, help='Select method')

    # webcam
    parser.add_argument('--id', type=int, required=False, help='Select id')

    parser.add_argument('--crossroad', type=str,
                        required=False, help='Select crossroad related')
    parser.add_argument('--active', type=str, required=False,
                        help='Select if active')

    # crossroad
    # also --active
    parser.add_argument('--name', type=str,
                        required=False, help='Select name')
    parser.add_argument('--lat', type=float, required=False,
                        help='Select latitude')
    parser.add_argument('--lon', type=float, required=False,
                        help='Select longitude')
    parser.add_argument('--traffic', type=float, required=False,
                        help='Select traffic level')
    parser.add_argument('--cars', type=str,
                        required=False, help='How many cars')

    # Street
    # also --name and --crossroad
    parser.add_argument('--length', type=int, required=False,
                        help='Select length')
    parser.add_argument('--alert', type=bool, required=False,
                        help='Select alert')

    # trafficlight
    # also --id and --crossroad
    parser.add_argument('--direction', type=str,
                        required=False, help='Select direction')
    parser.add_argument('--green', type=float,
                        required=False, help='Select green value')
    parser.add_argument('--street', type=str, required=False,
                        help='Select street related')

    args = parser.parse_args()

    email = args.email if args.email is not None else 'admin@admin.com'
    password = args.password if args.password is not None else 'admin'
    username = args.username if args.username is not None else 'admin'
    api = RestAPI(
        user={'email': email, 'password': password, 'username': username})

    if args.method == 'POST':
        data = fill_data(args)
        api.create_instance(args.model, data)

    elif args.method == 'GET':
        if args.model in ['webcam', 'trafficlight']:
            if args.id is not None:
                api.get_instance(args.model, args.id)
            else:
                api.get_instance(args.model)
        elif args.model in ['crossroad', 'street']:
            if args.name is not None:
                api.get_instance(args.model, args.name)

    elif args.method == 'PUT':
        data = fill_data(args)
        if args.model in ['webcam', 'trafficlight']:
            if args.id is not None:
                api.update_instance(args.model, args.id, data)
        elif args.model in ['crossroad', 'street']:
            if args.name is not None:
                api.update_instance(args.model, args.name, data)

    elif args.method == 'DELETE':
        if args.model in ['webcam', 'trafficlight']:
            if args.id is not None:
                api.delete_instance(args.model, args.id)
            else:
                print("Error: Argument --id must be provided")
                exit(1)
        elif args.model in ['crossroad', 'street']:
            if args.name is not None:
                api.delete_instance(args.model, args.name)
            else:
                print("Error: Argument --name must be provided")
                exit(1)
    else:
        print("Error: Method not found")
        exit(1)
