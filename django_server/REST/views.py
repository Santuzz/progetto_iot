from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import WebcamSerializer, CrossroadSerializer

from django.http import JsonResponse, HttpRequest

import json
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404


""" class WebcamCreateView(generics.CreateAPIView):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer

    # if you don't want to use the default queryset
    def get_queryset():
        return Webcam.objects.all()


class WebcamListCreateView(generics.ListCreateAPIView):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer """


def clean_crossroad(request):
    if 'crossroad_name' in request.data and request.data['crossroad_name'] is not None:
        request.data['crossroad_name'] = request.data['crossroad_name'].lower()
    return request


class WebcamAPI(APIView):
    # authentication
    # ...

    def get(self, request, pk=None):
        if pk is not None:
            obj = get_object_or_404(Webcam, pk=pk)
            data = WebcamSerializer(obj, many=False).data
            return Response(data, status=status.HTTP_200_OK)
        qs = Webcam.objects.all()
        data = WebcamSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        request = clean_crossroad(request)
        obj = get_object_or_404(Webcam, pk=pk)
        if 'crossroad' in request.data and request.data['crossroad'] is None:
            obj.crossroad = None
        serializer = WebcamSerializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"Invalid": "Impossible to serialize input data", "data": request.data}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        request = clean_crossroad(request)
        # takes data in input and
        serializer = WebcamSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"Invalid": "Impossible to serialize input data", "data": request.data}, status=status.HTTP_400_BAD_REQUEST)


class CrossroadAPI(APIView):
    # authentication
    # ...
    def get(self, request):
        try:
            name = request.data["name"].lower()
            instance = Crossroad.objects.get(name=name)
        except (Crossroad.DoesNotExist, KeyError):
            return JsonResponse({"error": f"Impossibile trovare l\'incrocio specificato"}, status=status.HTTP_404_NOT_FOUND)

        data = {}
        if instance:
            data = CrossroadSerializer(instance).data

        return Response(data, status=200)

    def post(self, request):
        serializer = CrossroadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(serializer.data)
        # togli raise exception da is_valid e definisci il comportamento se la richiesta fatta non è corretta
        # ovvero se non contiene dei valori corretti per creare una nuova instance
