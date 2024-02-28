import requests
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python basics_request.py <parameter>")
        return
    id = None
    param = sys.argv[1]
    if len(sys.argv) > 2:
        id = sys.argv[2]

    if param == "get":
        if id is None:
            print("Missing 'id' parameter")
            return
        # get request with id
        endpoint = f"http://localhost:8000/api/webcam/{id}/"

        get_response = requests.get(endpoint)
        print(get_response.json())
        return

    if param == "list":
        # get request without id
        endpoint = f"http://localhost:8000/api/webcam/"

        get_response = requests.get(endpoint)
        print(get_response.json())
        return

    if param == "post":
        endpoint = f"http://localhost:8000/api/webcam/"

        data = {
            "cars_count": 777,
            "active": True,
            "crossroad": "CIAO BELLO"
        }
        get_response = requests.post(endpoint, json=data)
        print(get_response.text)
        return

    if param == "put":
        if id is None:
            print("Missing 'id' parameter")
            return
        # get request with id
        endpoint = f"http://localhost:8000/api/webcam/{id}/"
        data = {
            "cars_count": 777,
            "active": False,

        }
        get_response = requests.put(endpoint, json=data)
        print(get_response.json())
        return

    print("Parameters didn't match.")


if __name__ == "__main__":
    main()
# ---------------- codice per API view django ------------------
# get a param from the request
# param = request.GET.get('abc')
# get the body from the request and convert to json
# body = request.body
# data = {}
# try:
#    data = json.loads(body)
# except:
#    pass
# get a dict from a model instance
# model_data = Webcam.objects.all().order_by('?').first()
# if model_data:
#    data = model_to_dict(model_data)
#    # add fields parameter to filter attributes
#    data = model_to_dict(model_data, fields=['id', 'cars_count'])
