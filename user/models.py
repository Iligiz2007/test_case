from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE = [
        ('user', 'Пользователь'),
        ('admin', 'Админ'),
    ]
    family_name = models.CharField(max_length=100)
    role = models.CharField(choices=ROLE,default='user')
    email = models.EmailField(unique=True,blank=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []