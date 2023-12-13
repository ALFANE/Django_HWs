from django.core.management import BaseCommand
from django.db.models import Q

from home.models import Student


class Command(BaseCommand):
    help = "Select students"

    def add_arguments(self, parser):
        parser.add_argument("-l", "--len", type=int, default=10)

    def handle(self, *args, **options):
        students = Student.objects.all().values()
        print(students)
