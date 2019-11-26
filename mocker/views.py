from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def mock_data(request, msg, format=None):
    return Response({"msg": "请求成功", "data": {"msg":msg}}, status=status.HTTP_200_OK)

