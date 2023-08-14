from django.db import models


# Create your models here.

class Student(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField()
