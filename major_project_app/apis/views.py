from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from meter_app import models
from .serializers import serializers_meter
class ListTodo(generics.ListCreateAPIView):
    queryset=models.meter.objects.all()
    serializer_class=serializers_meter
class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.meter.objects.all()
    serializer_class=serializers_meter


