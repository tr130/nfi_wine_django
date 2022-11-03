from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Register(APIView):
    def post(self, request, format=None):
        print(request.data)
        return Response({'register': 'received'})
