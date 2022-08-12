from django.db import models
from django.contrib.auth.models import AbstractUser



# To add extra content to user model.
class User(AbstractUser):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



# To make city data table.
class CityData(models.Model):
    name = models.CharField(max_length=255,unique=True)
    temperature = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

