from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import WebcamSerializer, CrossroadSerializer

from django.http import JsonResponse, HttpRequest

import json
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

import re

""" class WebcamCreateView(generics.CreateAPIView):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer

    # if you don't want to use the default queryset
    def get_queryset():
        return Webcam.objects.all()


class WebcamListCreateView(generics.ListCreateAPIView):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer """


def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass


def get_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise an Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)

    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(
                klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        klass__name = (klass.__name__ if isinstance(
            klass, type) else klass.__class__.__name__)
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return Response({"Invalid": "%s instance not found" % klass__name}, status=status.HTTP_404_NOT_FOUND)


def clean_crossroad(request):
    if 'crossroad_name' in request.data and request.data['crossroad_name'] is not None:
        request.data['crossroad_name'] = request.data['crossroad_name'].lower()
    return request


class WebcamDestroyView(generics.DestroyAPIView):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer()

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'Webcam successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)

# TODO utilizza funzione per controllare che cars_count sia una stringa di interi separati da una virgola


def check_string(in_string):
    pattern = r'^\d+(,\d+)*$'
    if re.match(pattern, in_string):
        return True
    else:
        return False


class WebcamAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            obj = get_object_or_404(Webcam, pk=pk)
            if isinstance(obj, Response):
                return obj
            data = WebcamSerializer(obj, many=False).data
            return Response(data, status=status.HTTP_200_OK)
        qs = Webcam.objects.all()
        data = WebcamSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        request = clean_crossroad(request)
        if 'cars_count' in request.data and not check_string(request.data['cars_count']):
            return Response({"Invalid": f"cars_count must be a string of integers separated by a comma, but instead it's {request.data['cars_count']}"}, status=status.HTTP_400_BAD_REQUEST)

        obj_wc = get_object_or_404(Webcam, pk=pk)
        if isinstance(obj_wc, Response):
            return obj_wc
        if 'crossroad_name' in request.data and request.data['crossroad_name'] is None:
            obj_wc.crossroad = None
        obj = get_object_or_404(Crossroad, name=request.data["crossroad_name"])
        if isinstance(obj, Response):
            return obj
        serializer = WebcamSerializer(obj_wc, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            # TODO questa due righe sotto servono a qualcosa???
            serializer_data = serializer.data
            serializer_data["crossroad"] = obj_wc.crossroad_id
            return Response(serializer_data, status=status.HTTP_202_ACCEPTED)
        return Response({"Invalid": "Impossible to serialize input data", "data": request.data}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        request = clean_crossroad(request)
        # takes data in input and
        if 'cars_count' in request.data and not check_string(request.data['cars_count']):
            return Response({"Invalid": f"cars_count must be a string of integers separated by a comma, but instead it's {request.data['cars_count']}"}, status=status.HTTP_400_BAD_REQUEST)
        obj = get_object_or_404(Crossroad, name=request.data["crossroad_name"])
        if isinstance(obj, Response):
            return obj
        serializer = WebcamSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            serializer_data = serializer.data
            serializer_data["crossroad"] = Webcam.objects.get(
                id=serializer.data["id"]).crossroad_id
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        return Response({"Invalid": "Impossible to serialize input data", "data": request.data}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        delete_view = WebcamDestroyView.as_view()
        # controllo se l'id esiste
        obj = get_object_or_404(Webcam, pk=pk)
        if isinstance(obj, Response):
            return obj
        response = delete_view(request._request, pk=pk)
        return Response({'message': 'Webcam successfully deleted.'}, status=status.HTTP_201_CREATED)


"""

{
    "name": "esempio_nome",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "creation_date": "2024-03-07T12:00:00",
    "traffic_level": 2.5,
    "active": True
}
"""


class CrossroadDestroyView(generics.DestroyAPIView):
    queryset = Crossroad.objects.all()
    serializer_class = CrossroadSerializer()

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'Crossroad successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)


class CrossroadAPI(APIView):
    # authentication
    # ...
    def get(self, request, name=None):
        if name is not None:
            try:
                # name = request.data["name"].lower()
                instance = Crossroad.objects.get(name=name.lower())
            except (Crossroad.DoesNotExist, KeyError):
                return JsonResponse({"Invalid": f"Impossible to find the specified crossroad"}, status=status.HTTP_404_NOT_FOUND)
            data = {}
            if instance:
                data = CrossroadSerializer(instance).data
            return Response(data, status=status.HTTP_200_OK)
        qs = Crossroad.objects.all()
        data = CrossroadSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        for key, value in request.data.items():
            if type(value) is str:
                request.data[key] = value.lower()
        serializer = CrossroadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(serializer.data)
        # togli raise exception da is_valid e definisci il comportamento se la richiesta fatta non è corretta
        # ovvero se non contiene dei valori corretti per creare una nuova instance

    def put(self, request, name=None):
        obj = get_object_or_404(Crossroad, pk=name.lower())
        if isinstance(obj, Response):
            return obj
        serializer = CrossroadSerializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"Invalid": "Impossible to serialize input data", "data": request.data}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None):
        delete_view = CrossroadDestroyView.as_view()
        # controllo se l'id esiste
        obj = get_object_or_404(Crossroad, pk=name.lower())
        if isinstance(obj, Response):
            return obj
        response = delete_view(
            request._request, pk=name.lower())
        return Response({'message': 'Crossroad successfully deleted.'}, status=status.HTTP_201_CREATED)


class CustomAuthToken(APIView):
    def get(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user = authenticate(request, email=email,
                            password=password, username=username)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
