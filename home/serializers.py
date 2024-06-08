from django.core.paginator import Paginator
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

    students = serializers.SerializerMethodField('pagination_students')
    # students = StudentSerializer(many=True)

    def pagination_students(self, obj):
        students = obj.students.all().order_by('name')

        pagination = Paginator(students, per_page=2)
        paginated_students = pagination.page(1)

        return StudentSerializer(instance=paginated_students, many=True).data
    """
        пагинация студентов для каждого учителя
    """
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'students']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']
