from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Commodity
from .serializers import CommoditySerializer


class CommodityListView(generics.ListAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.AllowAny]
    

class CommodityCreateView(generics.CreateAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.IsAdminUser]


class CommodityUpdateView(generics.UpdateAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.IsAdminUser]

