from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Commodity, Parameter, Grade, GradeParameter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from .serializers import CommodityListSerializer, CommodityCreateSerializer, ParameterCreateSerializer, ParameterListSerializer
from .serializers import ParameterUpdateSerializer, GradeParameterSerializer, CommodityGradeSerializer



class CommodityListAPIView(generics.ListAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommodityListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]
    

class CommodityCreateAPIView(generics.CreateAPIView):
    serializer_class = CommodityCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class CommodityUpdateAPIView(generics.UpdateAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommodityCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'pk' 


class CommodityDeleteAPIView(generics.DestroyAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommodityListSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'pk' 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False  
        instance.save()
        return super().destroy(request, *args, **kwargs)


class ParameterListAPIView(generics.ListAPIView):
   queryset = Parameter.active_objects.all()
   serializer_class = ParameterListSerializer
   permission_classes = [permissions.IsAuthenticated]
   pagination_class = PageNumberPagination
   filter_backends = [filters.SearchFilter]
   search_fields = ['name']
   def list(self, request, *args, **kwargs):
       queryset = self.filter_queryset(self.get_queryset())
       page = self.paginate_queryset(queryset)
       serializer = self.get_serializer(page, many=True)
       parameters = self.get_paginated_response(serializer.data)
       return Response(parameters.data)


class ParameterCreateAPIView(generics.CreateAPIView):
    serializer_class = ParameterCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ParameterDetailAPIView(generics.RetrieveAPIView):
   queryset = Parameter.active_objects.all()
   serializer_class = ParameterListSerializer
   permission_classes = [permissions.IsAuthenticated]
   lookup_field = 'pk'


class ParameterUpdateAPIView(generics.UpdateAPIView):
   queryset = Parameter.active_objects.all()
   serializer_class = ParameterUpdateSerializer
   permission_classes = [permissions.IsAdminUser]
   lookup_url_kwarg = 'pk'  


class ParameterDeleteAPIView(generics.DestroyAPIView):
   queryset = Parameter.active_objects.all()
   serializer_class = ParameterCreateSerializer
   permission_classes = [permissions.IsAdminUser]
   lookup_url_kwarg = 'pk' 
   def destroy(self, request, *args, **kwargs):
       instance = self.get_object()
       instance.is_active = False  
       instance.save()
       return super().destroy(request, *args, **kwargs)

   
class CommodityGradeCreateAPIView(generics.CreateAPIView):
    serializer_class = CommodityGradeSerializer
    permission_classes = [permissions.IsAdminUser]


class CommodityGradeListAPIView(generics.ListAPIView):
    queryset = Grade.active_objects.all()
    serializer_class = CommodityGradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class CommodityGradeDetailAPIView(generics.RetrieveAPIView):
    queryset = Grade.active_objects.all()
    serializer_class = CommodityGradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class CommodityGradeUpdateAPIView(generics.UpdateAPIView):
    queryset = Grade.active_objects.all()
    serializer_class = GradeParameterSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'pk' 



