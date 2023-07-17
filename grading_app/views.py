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
from .serializers import ParameterListSerializer, GradeParameterSerializer, CommodityGradeSerializer, CommodityGradeListSerializer



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
   


class CommodityGradeCreateAPIView(generics.CreateAPIView):
    queryset = CommodityGrade.active_objects.all()
    serializer_class = CommodityGradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
        response = {
            "message":"Commodity grades created successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
            
        

class CommodityGradeListAPIView(generics.ListAPIView):
    queryset = CommodityGrade.active_objects.all()
    serializer_class = CommodityGradeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    
class CommodityGradeDetailAPIView(generics.RetrieveAPIView):
    queryset = CommodityGrade.active_objects.all()
    serializer_class = CommodityGradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'commodity_name'
    

class CommodityGradeUpdateAPIView(generics.UpdateAPIView):
    queryset = CommodityGrade.active_objects.all()
    serializer_class = CommodityGradeUpdateSerializer

    def perform_update(self, serializer):
        commodity_grade = self.get_object()
        grade_parameters_data = self.request.data.get('grade_parameter', [])

        for param_data in grade_parameters_data:
            parameter = param_data['parameter']
            min_value = param_data['min_value']
            max_value = param_data['max_value']

            grade_parameter = commodity_grade.grade_parameter.get(parameter=parameter)
            grade_parameter.min_value = min_value
            grade_parameter.max_value = max_value
            grade_parameter.save()

        serializer.save()


