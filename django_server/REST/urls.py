from django.urls import path

from REST.views import *

app_name = "REST"
urlpatterns = [
    path('webcam/', WebCamAPI.as_view(), name='webcam-api'),

]
