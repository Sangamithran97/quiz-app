from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegsiterSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegsiterView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password', 'role'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'role': openapi.Schema(type=openapi.TYPE_STRING, description='admin or user'),
        }
    ))
    def post(self,request):
        v_serializer= RegsiterSerializer(data= request.data)

        if v_serializer.is_valid():
            v_serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(v_serializer.errors, status=400)