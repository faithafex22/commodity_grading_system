from rest_framework import serializers
from .models import Commodity, Parameter, Grade

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

        
class ParameterSerializer(serializers.ModelSerializer):
    commodities = CommodityNameSerializer(many=True, read_only=True)
    class Meta:
        model = Parameter
        fields = [ 'name', 'date_created', 'commodities']


class ParameterUpdateSerializer(serializers.ModelSerializer):
    commodities = CommodityNameSerializer(many=True)
    class Meta:
        model = Parameter
        fields = [ 'name', 'date_created', 'commodities']


class GradeCreateSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()
    commodity = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = ['commodity', 'parameter', 'value']

    def create(self, validated_data):
        parameter_data = validated_data.pop('parameter')
        parameter = Parameter.objects.get(name=parameter_data)
        grade = Grade.objects.create(parameter=parameter, **validated_data)
        return grade
