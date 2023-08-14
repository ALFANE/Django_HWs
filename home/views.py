from django.shortcuts import render
from django.http import HttpResponse
from faker import Faker
from home.models import Student

fake = Faker()

def hello(request):
    return HttpResponse(f'<h2>Hello World!</h2>')

def ShowAll(request):

    students = Student.objects.all()

    return render(
        request = request,
        template_name ='index.html',
        context = {
            'students': students,
        }
    )
