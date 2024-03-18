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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

from home.views import updateStudent, ShowAll, hello, create_student, create_student_by_form

from home.views_class import ShowAllView, AddNewStudentView, UpdateStudentView, AddStudentByNameView, DeleteStudentView, \
    ShowBookView, BookDeleteView, BookUpdateView, ShowSubjectView, SubjectDeleteView, SubjectUpdateView, \
    DeleteStudentFromSubjectView, AddStudentToSubjectView, ShowTeacherView, DeleteTeacherView, UpdateTeacherView, \
    DeleteStudentFromTeacher, AddStudentToTeacher, XMLView, JSONView, CSVView, FileView, SendMailview


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", hello),
    path("students/", ShowAll, name ='student_list'),
    path('student/update/<id>/', updateStudent, name = 'update_student'),
    path('student/create/', create_student, name = 'student_create'),
    path('student/form/create/', create_student_by_form, name = 'student_form_create'),

    path('class/students/',ShowAllView.as_view(), name = 'class_student_list'),
    path('class/student/delete/', DeleteStudentView.as_view(), name = 'class_student_delete'),
    path('class/student/create/', AddStudentByNameView.as_view(), name = 'class_student_create'),
    path('class/student/form/create/', AddNewStudentView.as_view(), name = 'class_student_form_create'),
    path('class/student/update/<pk>/', UpdateStudentView.as_view(), name = 'class_student_update'),

    path('class/books/', ShowBookView.as_view(), name = 'class_books_list'),
    path('class/book/delete/', BookDeleteView.as_view(), name = 'class_book_delete'),
    path('class/book/update/<pk>/', BookUpdateView.as_view(), name = 'class_book_update'),

    path('class/subjects/', ShowSubjectView.as_view(), name = 'class_subjects_list'),
    path('class/subject/delete/', SubjectDeleteView.as_view(), name = 'class_subject_delete'),
    path('class/subject/update/<pk>/', SubjectUpdateView.as_view(), name = 'class_subject_update'),
    path('class/subject_student/delete/', DeleteStudentFromSubjectView.as_view(), name = 'delete_student_from_subject'),
    path('class/subject_student/add/<subject_id>/', AddStudentToSubjectView.as_view(), name = 'add_student_to_subject'),

    path('class/teachers/', ShowTeacherView.as_view(), name = 'class_teachers_list'),
    path('class/teacher/delete/', DeleteTeacherView.as_view(), name = 'class_teacher_delete'),
    path('class/teacher/update/<id>/', UpdateTeacherView.as_view(), name = 'class_teacher_update'),
    path('class/teacher_student/delete/', DeleteStudentFromTeacher.as_view(), name = 'delete_student_from_teacher'),
    path('class/teacher_student/add/', AddStudentToTeacher.as_view() , name = 'add_student_to_teacher'),

    path('json_view', JSONView.as_view(), name = 'json_view'),
    path('csv_view', CSVView.as_view(), name = 'csv_view'),
    path('xml_view', XMLView.as_view(), name = 'xml_view'),
    path('file_view', FileView.as_view(), name = 'file_view'),

    path('send_email', SendMailview.as_view(), name = 'send_email_view'),

]
