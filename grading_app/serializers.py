from rest_framework import serializers
from .models import Commodity, Parameter, Grade,  GradeParameter


class CommodityListSerializer(serializers.ModelSerializer):
   class Meta:
       model = Commodity
       fields = ['name', 'image']


class CommodityCreateSerializer(serializers.ModelSerializer):
    parameters = serializers.StringRelatedField()
    class Meta:
        model = Commodity
        fields = ['name', 'parameters', 'image']
        
    
class ParameterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name']


class CommodityNameSerializer(serializers.ModelSerializer):
    class Meta:
      model = Commodity
      fields = ['name']

        
class ParameterListSerializer(serializers.ModelSerializer):
    commodities = CommodityNameSerializer(many=True, read_only=True)
    class Meta:
       model = Parameter
       fields = [ 'name', 'date_created', 'commodities']


class ParameterUpdateSerializer(serializers.ModelSerializer):
    commodities = CommodityNameSerializer(many=True)
    class Meta:
       model = Parameter
       fields = [ 'name', 'date_created', 'commodities']


class GradeParameterSerializer(serializers.ModelSerializer):
   class Meta:
       model = GradeParameter
       fields = ['parameter', 'min_value', 'max_value']
   

class CommodityGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['name', 'commodity', 'grade_parameter']



