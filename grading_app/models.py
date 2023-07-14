from django.db import models


# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class NonActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)

    

class Parameter(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    objects = models.Manager()  
    active_objects = ActiveManager()
    nonactive_objects = NonActiveManager()
    

class Commodity(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='grading_app/media', null=True, blank=True)
    parameters = models.ManyToManyField(Parameter)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    objects = models.Manager()
    active_objects = ActiveManager()
    nonactive_objects = NonActiveManager()

    @property
    def grade(self):
        average_value = self.parameters.aggregate(average=models.Avg('commodityparameter__value'))['average']
        
        if average_value >= 0 and average_value <= 5:
            return 1
        elif average_value >= 6 and average_value <= 10:
            return 2
        elif average_value >= 11 and average_value <= 15:
            return 3
        else:
            return 'Not accepted'

    
class Grade(models.Model):
    name = models.CharField(max_length=100, default='Input_grade_name')
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    grade_parameter = models.ForeignKey('GradeParameter', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.name} - {self.commodity}"

    objects = models.Manager()
    active_objects = ActiveManager()
    nonactive_objects = NonActiveManager()


class GradeParameter(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    min_value =  models.DecimalField(max_digits=3, decimal_places=1)
    max_value =  models.DecimalField(max_digits=3, decimal_places=1)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.parameter}"

    objects = models.Manager()
    active_objects = ActiveManager()
    nonactive_objects = NonActiveManager()




