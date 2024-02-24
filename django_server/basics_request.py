import requests

endpoint = "http://localhost:8000/api/crossroad/"

# get_response = requests.post(
#    endpoint, json={'cars_count': 12, 'active': True, 'crossroad': "stradella"})
# print(get_response.json())

data = {
    "name": "Stradella"
}
get_response = requests.get(endpoint, json=data)
print(get_response.json())


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
