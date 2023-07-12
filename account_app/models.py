from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)

class NonActiveManager(models.Manager):
    def get_queryset(self):
        return super(NonActiveManager, self).get_queryset().filter(is_active=False)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField( max_length=254, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_picture = models.ImageField(upload_to='account_app/media',  default='static/images/pi.png')
    phone_number = models.CharField(max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)
    state_code = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS= []
    USERNAME_FIELD = "email"

    objects = CustomUserManager()
    active_objects = ActiveManager()
    nonactive_objects = NonActiveManager()

    

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def picture_url(self):
        try:
            url = self.picture.url
        except:
            url =''
        return url


    def generate_user_id(self):
        state_code = self.state_code.upper() 
        year = str(timezone.now().year)
        unique_number = self.get_unique_number()  

        user_id = f"{state_code}/{year}/{unique_number}"
        return user_id

    def get_unique_number(self):
        last_user = User.active_users.order_by('-id').first()
        if last_user is None:
            return '0001'
        last_user_id = last_user.user_id.split('/')[-1]
        new_number = str(int(last_user_id) + 1).zfill(4)
        return new_number
