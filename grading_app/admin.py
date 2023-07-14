from django.contrib import admin
from grading_app.models import Parameter, Commodity, Grade, GradeParameter

# Register your models here.
admin.site.register(Parameter)
admin.site.register(Commodity)
admin.site.register(Grade)
admin.site.register(GradeParameter)




