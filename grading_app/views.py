from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Commodity, Parameter, CommodityGrade, GradeParameter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.exceptions import NotFound
from .serializers import CommodityListSerializer, CommodityCreateSerializer, ParameterCreateSerializer , CommodityGradeUpdateSerializer
from .serializers import ParameterListSerializer,  CommodityGradeSerializer, CommodityGradeListSerializer



class CommodityListAPIView(generics.ListAPIView):
    queryset = Commodity.active_objects.all()
    serializer_class = CommodityListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]
    

class CommodityDetailAPIView(generics.RetrieveAPIView):
   queryset = Commodity.active_objects.all()
   serializer_class = CommodityCreateSerializer
   permission_classes = [permissions.IsAuthenticated]
   lookup_field = 'pk'


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
        self.perform_destroy(instance)
        return Response({"message": "Commodity successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    


class ParameterListAPIView(generics.ListAPIView):
   queryset = Parameter.active_objects.all()
   serializer_class = ParameterListSerializer
   permission_classes = [permissions.IsAuthenticated]
   pagination_class = PageNumberPagination
   pagination_class.page_size = 10  
   filter_backends = [filters.SearchFilter]
   search_fields = ['name']

   def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    

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
   serializer_class = ParameterCreateSerializer
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
       self.perform_destroy(instance)
       return Response({"message": "Commodity successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
   

class CommodityGradeListCreateView(generics.ListCreateAPIView):
    queryset = CommodityGrade.objects.all()
    serializer_class = CommodityGradeSerializer

    def perform_create(self, serializer):
        grade_parameters_data = self.request.data.pop('grade_parameters', [])
        grade_parameters = []
        for parameter_data in grade_parameters_data:
            grade_parameters.append(GradeParameter.objects.get_or_create(**parameter_data)[0])
        serializer.save(grade_parameters=grade_parameters)
    

class CommodityGradeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommodityGrade.objects.all()
    serializer_class = CommodityGradeSerializer

    def perform_update(self, serializer):
        grade_parameters_data = self.request.data.get('grade_parameters', [])
        grade_parameters = []
        for parameter_data in grade_parameters_data:
            grade_parameters.append(GradeParameter.objects.get_or_create(**parameter_data)[0])
        serializer.save(grade_parameters=grade_parameters)

    