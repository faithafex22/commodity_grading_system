from django.contrib import admin
from grading_app.models import Parameter, Commodity, CommodityGrade, GradeParameter

# Register your models here.
admin.site.register(Parameter)
admin.site.register(Commodity)
admin.site.register(CommodityGrade)
admin.site.register(GradeParameter)




