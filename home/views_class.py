import requests
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse

from app.celery import test_task_celery
from home.tasks import test_task_celery2, compile_task
from home.models import Student
from home.forms import StudentForm


class ShowAllView(View):

    def get(self, request):

        test_task_celery.delay()
        test_task_celery2.delay()
        compile_task.delay()

        students = Student.objects.all()
        # stdent_form = StudentForm('id')
        context = {
            "students": students,
            # 'form': stdent_form,
        }
        return render(
            request=request,
            template_name="index.html",
            context=context
        )


class AddStudentByNameView(View):

    def get(self, request):

        student_name_from_request = request.GET.get('name')
        if not student_name_from_request:
            return HttpResponse('Student name missing')

        student = Student()
        student.name = student_name_from_request
        student.save()

        return HttpResponse('Student {} have been created'.format(student.name))

class AddNewStudentView(View):

    def get(self, request):

        student_form = StudentForm()
        context = {
            'form': student_form,
        }

        return render(
            request=request,
            template_name='student_form.html',
            context = context,
        )

    def post(self, request):

        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()

        return redirect(reverse('class_student_list'))

class DeleteStudentView(View):

    def get(self, request):

        student_id = request.GET.get('id')
        if not student_id:
            return HttpResponse('Missing student id')
        student = Student.objects.get(id=student_id)
        student.delete()

        return redirect(reverse('class_student_list'))

class UpdateStudentView(View):

    def get(self, request, id):

        student = get_object_or_404(Student, id=id)
        student_form = StudentForm(instance=student)
        context = {
            'form': student_form,
            'student': student,
        }
        return render(
            request = request,
            template_name= 'student_update.html',
            context = context
        )

    def post(self, request, id):

        student = get_object_or_404(Student, id=id)
        student_form = StudentForm(request.POST, instance = student)

        if student_form.is_valid():
            student_form.save()

        return redirect(reverse('class_student_list'))



