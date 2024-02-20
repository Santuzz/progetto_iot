from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET','POST','DELETE'])
class WebCamAPI(APIView):


    
