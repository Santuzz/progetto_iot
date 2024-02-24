from django.urls import path

from REST.views import *

app_name = "REST"

urlpatterns = [
    path('webcam/<int:pk>/', WebcamAPI.as_view(), name='webcam-api-pk'),
    # path('webcam/', WebcamCreateView.as_view(), name='webcam-create'), split in two row below
    path('webcam/', WebcamAPI.as_view(), name='webcam-api'),
    path('webcam/create/', WebcamCreateView.as_view(), name='webcam-create'),
    path('crossroad/<int:pk>/', CrossroadAPI.as_view(), name='crossroad-api-pk'),
    path('crossroad/', CrossroadAPI.as_view(), name='crossroad-api'),

]
