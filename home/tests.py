import uuid
from unittest import skip

from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

from home.models import Book, Student, Subject, Teacher
from home.tasks import sum_number
from rest_framework.test import APITestCase


# Create your tests here.
# class HomeUnittest(TestCase):
#
#     @skip('unlock_soon')
#     def test_sum_numbers_in_tasks(self):
#
#         sum = sum_number(2, 2, 2)
#         self.assertEqual(sum, 6)
#
#     def test_sum_numbers_in_tasks2(self):
#         sum = sum_number(2, 2, 2)
#         self.assertEqual(sum, 6)
#
#     def test_sum_numbers_in_tasks3(self):
#
#         sum = sum_number(2, 2, 3)
#         self.assertEqual(sum, 6)

# class TeacherApiTests(APITestCase):
#
#     def test_get_teachers_list(self):
#
#
#         response = self.client.get(reverse('teachers_api_viewset-list'))
#         self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})

class StudentApiTests(APITestCase):

    def setUp(self):

        self.faker = Faker()
        student = Student()
        student.name = self.faker.first_name()
        student.surname = self.faker.last_name()
        student.age = self.faker.pyint(min_value=16, max_value=60, step=1)
        student.gender = self.faker.simple_profile()["sex"]
        student.email = self.faker.email()
        student.save()
        self.student_id = student.id

    def test_insert_create_student(self):

        response = self.client.post(reverse('students_api_viewset-list'),
                                    data={
                                        'name': self.faker.first_name(),
                                        'surname': self.faker.last_name(),
                                        'age': self.faker.pyint(min_value=16, max_value=60, step=1),
                                        'gender': self.faker.simple_profile()["sex"],
                                        'email': self.faker.email(),
                                    }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data['name'], response.data['name'])
        self.assertEqual(response_data['surname'], response.data['surname'])
        self.assertEqual(response_data['age'], response.data['age'])
        self.assertEqual(response_data['gender'], response.data['gender'])
        self.assertEqual(response_data['email'], response.data['email'])
        print('запрос после создания', response.json())

    def test_select_read_student(self):

        response = self.client.get(reverse('students_api_viewset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertNotEqual(response_data, {'count': 0, 'next': None, 'previous': None, 'results': []})
        self.assertEqual(response_data['count'], 1)
        student_data = response_data['results'][0]
        self.assertEqual(student_data['id'], self.student_id)
        self.assertEqual(student_data['name'], Student.objects.get(id=self.student_id).name)

    def test_update_student(self):

        student = Student.objects.get(id=self.student_id)
        print('before', student.name)
        new_name = self.faker.first_name()
        print('new', new_name)
        response = self.client.put(reverse('students_api_viewset-detail', args=[self.student_id]),
                                      data={
                                          'name': new_name,
                                      }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        student = Student.objects.get(id=self.student_id)
        print('after', student.name)

    def test_delete_student(self):

        response = self.client.delete(reverse('students_api_viewset-detail', args=[self.student_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        students = Student.objects.all()
        self.assertEqual(students.count(), 0)

class SubjectApiTests(APITestCase):

    def setUp(self):

        self.faker = Faker()
        subject = Subject.objects.create(title=self.faker.job())
        self.subject_id = subject.id

    def test_insert_create_subject(self):

        response = self.client.post(reverse('subjects_api_viewset-list'),
                                    data={
                                        'title': self.faker.job(),
                                    }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data['title'], response.data['title'])

    def test_select_read_subject(self):

        response = self.client.get(reverse('subjects_api_viewset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertNotEqual(response_data, {'count': 0, 'next': None, 'previous': None, 'results': []})
        self.assertEqual(response_data['count'], 1)
        subject_data = response_data['results'][0]
        self.assertEqual(subject_data['id'], self.subject_id)
        self.assertEqual(subject_data['title'], Subject.objects.get(id=self.subject_id).title)
    def test_update_subject(self):

        subject = Subject.objects.get(id=self.subject_id)
        new_title = self.faker.job()
        response = self.client.put(reverse('subjects_api_viewset-detail', args=[self.subject_id]),
                                    data={
                                        'title': new_title,
                                    }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subject(self):

        response = self.client.delete(reverse('subjects_api_viewset-detail', args=[self.subject_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        subjects = Subject.objects.all()
        self.assertEqual(subjects.count(), 0)



class TeacherApiTests(APITestCase):

    def setUp(self):

        self.faker = Faker()
        teacher = Teacher.objects.create(name=self.faker.name())
        self.teacher_id = teacher.id

    def test_insert_create_teacher(self):

        response = self.client.post(reverse('teachers_api_viewset-list'),
                                    data={
                                        'name': self.faker.name(),
                                    }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data['name'], response.data['name'])

    def test_select_read_teacher(self):

        response = self.client.get(reverse('teachers_api_viewset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertNotEqual(response_data, {'count': 0, 'next': None, 'previous': None, 'results': []})
        self.assertEqual(response_data['count'], 1)
        teacher_data = response_data['results'][0]
        self.assertEqual(teacher_data['id'], self.teacher_id)
        self.assertEqual(teacher_data['name'], Teacher.objects.get(id=self.teacher_id).name)

    def test_update_teacher(self):

        new_name = self.faker.name()
        response = self.client.put(reverse('teachers_api_viewset-detail', args=[self.teacher_id]),
                                   data={
                                       'name': new_name,
                                   }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_teacher(self):

        response = self.client.delete(reverse('teachers_api_viewset-detail', args=[self.teacher_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        teachers = Teacher.objects.all()
        self.assertEqual(teachers.count(), 0)

class BookApiTests(APITestCase):

    def setUp(self):

        book = Book.objects.create(title=uuid.uuid4())
        self.book_id = book.id

    def test_insert_create_book(self):

        response = self.client.post(reverse('books_api_viewset-list'),
                                    data={
                                        'title': uuid.uuid4(),
                                    }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data['title'], response.data['title'])

    def test_select_read_book(self):

        response = self.client.get(reverse('books_api_viewset-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertNotEqual(response_data, {'count': 0, 'next': None, 'previous': None, 'results': []})
        self.assertEqual(response_data['count'], 1)
        book_data = response_data['results'][0]
        self.assertEqual(book_data['id'], self.book_id)
        self.assertEqual(book_data['title'], Book.objects.get(id=self.book_id).title)


    def test_update_book(self):

        new_title = uuid.uuid4()
        response = self.client.put(reverse('books_api_viewset-detail', args=[self.book_id]),
                                   data={
                                       'title': new_title,
                                   }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):

        response = self.client.delete(reverse('books_api_viewset-detail', args=[self.book_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        books = Book.objects.all()
        self.assertEqual(books.count(), 0)
