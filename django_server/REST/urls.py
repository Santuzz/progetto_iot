from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from REST.views import *
from init_db import *


app_name = "REST"

urlpatterns = [

    path('auth/', obtain_auth_token),
    path('webcam/<int:pk>/', WebcamAPI.as_view(), name='webcam-api-detail'),
    path('webcam/', WebcamAPI.as_view(), name='webcam-api'),

    path('crossroad/<str:name>/', CrossroadAPI.as_view(),
         name='crossroad-api-detail'),
    path('crossroad/', CrossroadAPI.as_view(), name='crossroad-api'),

    path('token/', CustomAuthToken.as_view(), name='token-api'),
]

# inserire qui gli script utili per quando viene avviato il server

# erase_db()
# init_db()
