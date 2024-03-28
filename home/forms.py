from django.forms import ModelForm

from home.models import Student, Book, Subject, Teacher


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["name", "surname", "age", "gender", "email"]

class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['title']

class SubjectForm(ModelForm):

    class Meta:
        model = Subject
        fields = ['title']

class TeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ['name']