from django.urls import path

from REST.views import *

app_name = "REST"

urlpatterns = [
    path('webcam/<int:pk>/', WebcamAPI.as_view(), name='webcam-api-detail'),
    path('webcam/', WebcamAPI.as_view(), name='webcam-api'),
    path('crossroad/<int:pk>/', CrossroadAPI.as_view(), name='crossroad-api-pk'),
    path('crossroad/', CrossroadAPI.as_view(), name='crossroad-api'),

]
