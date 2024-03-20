import requests
import datetime
import argparse


class RestAPI:
    def __init__(self, user, base_url='http://localhost:8000/api/'):
        self.base_url = base_url
        self.user = user
        if user.get('password') is None or (user.get('username') is None and user.get('email') is None):
            raise Exception(
                'Errore: è necessario specificare password e almeno uno tra email o username')
        self.token = self.get_auth_token()

    def get_auth_token(self):
        token_url = self.base_url + 'token/'
        response = requests.get(token_url, data={'password': self.user.get(
            'password'), 'email': self.user.get('email'), 'username': self.user.get('username')})
        print({'password': self.user.get('password'), 'email': self.user.get(
            'email'), 'username': self.user.get('username')})
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print(f"Failed to get token. Status code: {response.status_code}")
            print(response.json())
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
        print(response.status_code)
        print(response.json())

    def delete_instance(self, model_name, id):
        url = f'{model_name.lower()}/{id}/'
        response = self.request('DELETE', url)
        print(response.status_code)
        try:
            print(response.json())
        except:
            pass

    def update_instance(self, model_name, id, data):
        url = f'{model_name.lower()}/{id}/'
        response = self.request('PUT', url, data)
        print(response.status_code)
        print(response.json())

    def get_instance(self, model_name, id):
        url = f'{model_name.lower()}/{id}/'
        response = self.request('GET', url)
        print(response.status_code)
        print(response.json())

    def send_count(self, crossroad, cars_count):
        url = f'webcam/'
        # convert from list to string
        cars_count = ", ".join(str(num) for num in cars_count)
        last_send = self.get_current_date()
        data = {"cars_count": cars_count,
                "last_send": last_send,
                "crossroad_name": crossroad}
        response = self.request('POST', url, data)
        print(response.status_code)
        print(response.json())


def fill_data(args):
    data = {
        'id': None,
        'cars': None,
        'crossroad_name': None,
        'active': None,
        'crossroad': None,
        'latitude': None,
        'longitude': None,
        'street': None,
        'length': None,
        'alert': None,
        'direction': None,
        'green_value': None,
        'street_name': None
    }
    if args.model == 'webcam':
        if args.crossroad is not None:
            data['crossroad_name'] = args.crossroad
        if args.active is not None:
            data['active'] = args.active
        elif args.crossroad is None:
            print(
                "Error: provide at least --crossroad or --active for a webcam")
            exit(1)

    elif args.model == 'crossroad':
        if args.name is not None:
            data['crossroad'] = args.name
        else:
            print("Error: Argument --name must be provided for a crossroad")
            exit(1)
        if args.active is not None:
            data['active'] = args.active
        if args.lat is not None:
            data['latitude'] = args.lat
        if args.lon is not None:
            data['longitude'] = args.lon

    elif args.model == 'street':
        if args.name is not None:
            data['crossroad'] = args.name
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
                "Error: provide at least --crossroad, --direction, --green or --street for a trafficlight")
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
        '--model', choices=['webcam', 'Crossroad', 'Street', 'Trafficlight'], required=True, help='Select model')
    parser.add_argument(
        '--method', choices=['get', 'create', 'update', 'delete'], required=True, help='Select method')

    # webcam
    parser.add_argument('--id', type=int, required=False, help='Select id')
    parser.add_argument('--cars', type=str,
                        required=False, help='How many cars')
    parser.add_argument('--crossroad', type=str,
                        required=False, help='Select crossroad related')
    parser.add_argument('--active', type=bool, required=False,
                        help='Select if active')

    # crossroad
    # also --active
    parser.add_argument('--name', type=str,
                        required=False, help='Select name')
    parser.add_argument('--lat', type=float, required=False,
                        help='Select latitude')
    parser.add_argument('--lon', type=float, required=False,
                        help='Select longitude')

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

    if args.method == 'create':
        data = fill_data(args)
        api.create_instance(args.model, data)

    if args.method == 'get':
        if args.model in ['webcam', 'Trafficlight']:
            if args.id is not None:
                api.get_instance(args.model, args.id)
        elif args.model in ['Crossroad', 'Street']:
            if args.name is not None:
                api.get_instance(args.model, args.name)

    if args.method == 'update':
        fill_data(args)
        api.update_instance(args.model, data)

    if args.method == 'delete':
        if args.model in ['webcam', 'Trafficlight']:
            if args.id is not None:
                api.delete_instance(args.model, args.id)
            else:
                print("Error: Argument --id must be provided")
                exit(1)
        elif args.model in ['Crossroad', 'Street']:
            if args.name is not None:
                api.delete_instance(args.model, args.name)
            else:
                print("Error: Argument --name must be provided")
                exit(1)
    else:
        print("Error: Method not found")
        exit(1)
