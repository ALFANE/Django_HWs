from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from home.models import Student
from home.forms import StudentForm


def hello(request):
    return HttpResponse(f"<h2>Hello World!</h2>")


def ShowAll(request):
    if request.method == "GET":
        students = Student.objects.all()
        context = {
            "students": students,
        }
        return render(
            request=request,
            template_name="index.html",
            context=context
        )


def create_student(request):
    student_name_from_request = request.GET.get('name')
    if not student_name_from_request:
        return HttpResponse('Student name missing')

    student = Student()
    student.name = student_name_from_request
    student.save()

    return HttpResponse('Student {} have been created'.format(student.name))

def create_student_by_form(request):
    if request.method == 'GET':
        student_form = StudentForm()
        context = {
            'form': student_form,
        }

        return render(
            request=request,
            template_name='student_form.html',
            context=context,
        )

    elif request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
            return redirect(reverse('student_list'))


def updateStudent(request, id):

    if request.method == "GET":
        student = Student.objects.get(id=id)
        student_form = StudentForm(instance = student)
        context = {
            "form": student_form,
            'student_id': student.id,

        }
        return render(
            request=request,
            template_name="student_update.html",
            context=context
        )

    elif request.method == "POST":

        student = Student.objects.get(id=id)

        student_form = StudentForm(request.POST, instance = student)

        if student_form.is_valid():
            student_form.save()

            return redirect(reverse('students_list'))

        else:
            return HttpResponseBadRequest('ERROR')