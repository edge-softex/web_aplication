from django.shortcuts import render
from rest_framework import viewsets

from .serializers import PVDataSerializer, PowerForecastSerializer, YieldDaySerializer, YieldMonthSerializer
from .models import PVData, PowerForecast, YieldDay, YieldMonth

# Create your views here.

class PVViewSet(viewsets.ModelViewSet):
    serializer_class = PVDataSerializer
    queryset = PVData.objects.all()

class PowerForecastSet(viewsets.ModelViewSet):
    serializer_class = PowerForecastSerializer
    queryset = PowerForecast.objects.all()

class YieldDaySet(viewsets.ModelViewSet):
    serializer_class = YieldDaySerializer
    queryset = YieldDay.objects.all()

class YieldMonthSet(viewsets.ModelViewSet):
    serializer_class = YieldMonthSerializer
    queryset = YieldMonth.objects.all()