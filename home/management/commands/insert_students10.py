import sys
import uuid

from django.core.management import BaseCommand

from home.models import Student, Subject, Book, Teacher
from faker import Faker


class Command(BaseCommand):
    help = "Insert 10 new sudents to the system"

    def add_arguments(self, parser):
        parser.add_argument("-l", "--len", type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker()
        # print(args)
        # print(options)
        sys.stdout.write("Start inserting Students \n")

        for _ in range(options["len"]):
            book = Book()
            book.title = uuid.uuid4()
            book.save()

            subject, _ = Subject.objects.get_or_create(title=faker.job())
            subject.save() 

            student = Student()
            student.name = faker.first_name()
            student.surname = faker.last_name()
            student.age = faker.pyint(min_value=16, max_value=60, step=1)
            # student.gender = faker.simple_profile()["sex"]
            student.address = faker.address()
            student.description = faker.text()
            student.birthday = faker.date_between(start_date="-60y", end_date="-16y")
            student.email = faker.email()
            student.social_url = student.name + student.surname + '@mail.com'
            student.book = book
            student.subject = subject
            student.save()

            teacher, _ = Teacher.objects.get_or_create(name=faker.name())
            teacher.students.add(student)
            teacher.save()

        sys.stdout.write("End inserting Students \n")
