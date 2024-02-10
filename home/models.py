from django.db import models


# Create your models here.


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    normalized_name = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    email = models.EmailField(null=True)
    social_url = models.URLField(null=True)
    is_active = models.CharField(max_length=20, null=True)
    subject = models.ForeignKey('home.Subject', on_delete=models.SET_NULL, null=True) #одиин ко многим
    book = models.OneToOneField('home.Book', on_delete=models.CASCADE, null=True) #один к одному

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField('home.Student') #многие ко многим

