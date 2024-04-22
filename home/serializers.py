from rest_framework import serializers

from home.models import Student, Subject, Teacher, Book


class StudentSerializer(serializers.ModelSerializer):
    subject_title = serializers.CharField(source='subject.title', read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'surname', 'age', 'gender', 'email', 'subject_title', 'picture']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']

class TeacherSerializer(serializers.ModelSerializer):

    students = StudentSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'students']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']
