from django.contrib import admin
from grading_app.models import Parameter, Commodity,  Selected_Parameter, Grade

# Register your models here.
admin.site.register(Parameter)
admin.site.register(Commodity)
admin.site.register(Selected_Parameter)
admin.site.register(Grade)



