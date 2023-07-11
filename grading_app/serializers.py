from rest_framework import serializers
from .models import Commodity, Parameter

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):
    commodities = CommoditySerializer(many=True, read_only=True)

    class Meta:
        model = Parameter
        fields = ['id', 'name', 'commodities']