from django.shortcuts import render, redirect
from django.http import HttpResponse
from faker import Faker
from home.models import Student
from home.forms import StudentForm


def hello(request):
    return HttpResponse(f'<h2>Hello World!</h2>')

def ShowAll(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_form = StudentForm()
        context = {
                'students': students,
                'form': student_form,
            }
        return render(
            request = request,
            template_name ='index.html',
            context = context
        )
    elif request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
        return redirect('/showall/')
