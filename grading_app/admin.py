from django.contrib import admin
from grading_app.models import Parameter, Commodity,  CommodityParameter, Grade

# Register your models here.
admin.site.register(Parameter)
admin.site.register(Commodity)
admin.site.register(CommodityParameter)
admin.site.register(Grade)