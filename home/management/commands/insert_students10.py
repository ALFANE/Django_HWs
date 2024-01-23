import sys

from django.core.management import BaseCommand

from home.models import Student
from faker import Faker


class Command(BaseCommand):
    help = "Insert 10 new sudents to the system"

    def add_arguments(self, parser):
        parser.add_argument("-l", "--len", type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker("uk_UA")
        # print(args)
        # print(options)
        sys.stdout.write("Start inserting Students \n")

        for _ in range(options["len"]):
            student = Student()
            student.name = faker.first_name()
            student.surname = faker.last_name()
            student.age = faker.pyint(min_value=16, max_value=60, step=1)
            student.gender = faker.simple_profile()["sex"]
            student.address = faker.address()
            student.description = faker.text()
            student.birthday = faker.date_between(start_date="-60y", end_date="-16y")
            student.email = faker.email()
            student.social_url = student.name + student.surname + '@mail.com'
            student.save()
        sys.stdout.write("End inserting Students \n")
