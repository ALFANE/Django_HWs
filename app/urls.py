"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from home.views import updateStudent, ShowAll, hello, create_student, create_student_by_form

from home.views_class import ShowAllView, AddNewStudentView, UpdateStudentView, AddStudentByNameView, DeleteStudentView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", hello),
    path("students/", ShowAll, name ='student_list'),
    path('student/update/<id>/', updateStudent, name = 'update_student'),
    path('student/create/', create_student, name = 'student_create'),
    path('student/form/create/', create_student_by_form, name = 'student_form_create'),

    path('class/student/delete/', DeleteStudentView.as_view(), name = 'class_student_delete'),
    path('class/students/', ShowAllView.as_view(), name = 'class_student_list'),
    path('class/student/create/', AddStudentByNameView.as_view(), name = 'class_student_create'),
    path('class/student/form/create/', AddNewStudentView.as_view(), name = 'class_student_form_create'),
    path('class/student/update/<id>/', UpdateStudentView.as_view(), name = 'class_student_update')
]
