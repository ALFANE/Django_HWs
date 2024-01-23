from django.forms import ModelForm

from home.models import Student


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["name", "surname", "age", "gender", "email"]
