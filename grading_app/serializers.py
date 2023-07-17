from rest_framework import serializers
from .models import Commodity, Parameter, CommodityGrade,  GradeParameter


class CommodityListSerializer(serializers.ModelSerializer):
   class Meta:
       model = Commodity
       fields = ['name', 'image']


class CommodityCreateSerializer(serializers.ModelSerializer):
    parameters = serializers.PrimaryKeyRelatedField(queryset=Parameter.active_objects.all(), many=True)

    class Meta:
        model = Commodity
        fields = ['name', 'parameters', 'image']
        
    
class ParameterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name']



class ParameterListSerializer(serializers.ModelSerializer):
    commodities = serializers.SerializerMethodField()

    class Meta:
        model = Parameter
        fields = ('id', 'name', 'commodities')

    def get_commodities(self, parameter):
        commodities = parameter.commodity_set.values_list('name', flat=True)
        return list(commodities)



class GradeParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeParameter
        fields = ('parameter', 'min_value', 'max_value')



class CommodityGradeSerializer(serializers.ModelSerializer):
    grade_parameter = GradeParameterSerializer(many=True)
    class Meta:
        model = CommodityGrade
        fields = ('name', 'grade_parameter')



class CommodityGradeListSerializer(serializers.ModelSerializer):
    grade_parameter = GradeParameterSerializer(many=True)

    class Meta:
        model = CommodityGrade
        fields = ('name',)



class CommodityGradeUpdateSerializer(serializers.ModelSerializer):
    grade_parameter = GradeParameterSerializer(many=True)

    class Meta:
        model = CommodityGrade
        fields = ('grade_parameter',)




