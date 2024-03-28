import sys

from django.core.management import BaseCommand

from home.models import Student, Subject, Book, Teacher
from faker import Faker


class Command(BaseCommand):
    help = "Delete 10  sudents from system"



    def handle(self, *args, **options):

        students = Student.objects.all()
        students.delete()
        book = Book.objects.all()
        book.delete()
        teacher = Teacher.objects.all()
        teacher.delete()
        subject = Subject.objects.all()
        subject.delete()
        sys.stdout.write('Students has been deleted \n')


