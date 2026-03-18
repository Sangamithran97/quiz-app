from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegsiterSerializer
# Create your views here.

class RegsiterView(APIView):
    def post(self,request):
        v_serializer= RegsiterSerializer(data= request.data)

        if v_serializer.is_valid():
            v_serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(v_serializer.errors, status=400)