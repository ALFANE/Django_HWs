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
    picture = models.ImageField(upload_to='student_photos/', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    subject = models.ForeignKey(
        to = 'home.Subject',
        on_delete=models.SET_NULL,
        null=True,
        related_name = 'students', # позволяет изменять имя для обратного обращение к модели с student_set (modelname_set) на students
        related_query_name = 'students', # позволяет изменять имя для обратной связи к модели в запросе с student на students
    ) #одиин ко многим
    book = models.OneToOneField(
        to = 'home.Book',
        on_delete=models.CASCADE,
        null=True,
        related_name = 'student',
        related_query_name = 'student'
    ) #один к одному

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    students = models.ManyToManyField(
        to = 'home.Student',
        related_name = 'teachers',
        related_query_name = 'teachers'
    ) #многие ко многим

class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    ccy = models.CharField(max_length=30, null=True)
    buy = models.FloatField(null=True)
    sale = models.FloatField(null=True)