from django.db import models


# Create your models here.


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=6, null=True)
    address = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    email = models.EmailField(null=True)
    social_url = models.URLField(null=True)
