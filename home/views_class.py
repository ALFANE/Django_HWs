import csv
import uuid
from time import sleep

import django_filters
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db import transaction
from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, FileResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from app import utils
from app.celery import test_task_celery
from app.utils import send_student_email
from home.emails import send_email
from home.paginations import StudentPagination
from home.serializers import StudentSerializer, SubjectSerializer, TeacherSerializer, BookSerializer
from home.tasks import test_task_celery2, compile_task
from home.models import Student, Book, Subject, Teacher
from home.forms import StudentForm, BookForm, SubjectForm, TeacherForm, UserSignUpForm


class StartPage(View):

    def get(self, request):
        return render(
            request = request,
            template_name= 'start_page.html'
        )

class SignUpView(View):

    def get(self, request):

        sign_up_form = UserSignUpForm()
        context = {
            'form': sign_up_form,
        }

        return render(
            request = request,
            template_name = 'sign_up.html',
            context = context
        )

    def post(self, request):

        sign_up_form = UserSignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            user.is_active = False
            user.set_password(request.POST['password1'])
            user.save()

            current_site = get_current_site(request)
            domain = current_site.domain
            print(current_site)
            print(domain)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # activate_url = '{}/{}/{}'.format(
            #     'http://localhost:8001/activate',
            #     uid,
            #     default_token_generator.make_token(user=user)
            # )
            activate_url = 'http://{}/activate/{}/{}'.format(
                domain,
                uid,
                default_token_generator.make_token(user=user)
            )
            send_email(
                recipient_list=[user.email],
                activate_url=activate_url
            )
            return HttpResponse('Check yoor email to activate your account!')
        return HttpResponse('Wrong data!')
class ActivateView(View):

    def get(self, request, uid, token):

        user_id = force_bytes(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        if not user.is_active and default_token_generator.check_token(user, token):

            user.is_active = True
            user.save()
            login(request, user)

            return HttpResponse('Token checked. Your account has been activated')

        return HttpResponse('Your account already activated')

class SignInView(View):

    def get(self, request):

        sign_in_form = AuthenticationForm()
        context = {
            'form': sign_in_form,
        }

        return render(
            request = request,
            template_name = 'sign_in.html',
            context = context
        )

    def post(self, request):

        # sign_in_form = AuthenticationForm(request.POST.get)
        # print(sign_in_form)
        user_a = authenticate(
            request = request,
            username = request.POST.get('username'),
            password = request.POST.get('password')
        )
        login(request, user_a)

        return redirect(reverse('start_page'))
class SignOutView(View):

    def get(self, request):

        logout(request)
        print(request.user)
        return redirect(reverse('start_page'))

# @method_decorator(cache_page(settings.CACHE_TTL), name='dispatch')
class ShowAllView(View):

    def get(self, request):

        if request.user.is_authenticated:

            # test_task_celery.delay()
            # test_task_celery2.delay()
            # compile_task.delay()
            if request.GET.get('teacher_name'):

                teacher_name = request.GET.get('teacher_name')
                students = Student.objects.filter(teachers__name=teacher_name)
                context = {
                    'students': students,
                }

                return render(
                    request=request,
                    template_name="index.html",
                    context=context
                )

            elif request.GET.get('subject_name'):

                subject_name = request.GET.get('subject_name')
                students = Student.objects.filter(subject__title=subject_name)
                context = {
                    "students": students,
                }

                return render(
                    request=request,
                    template_name="index.html",
                    context=context
                )

            elif request.GET.get('book_number'):

                book_number = request.GET.get('book_number')
                students = Student.objects.filter(book__title=book_number)
                print(students)
                context = {
                    "students": students,
                }

                return render(
                    request=request,
                    template_name="index.html",
                    context=context
                )

            else:

                # В основном для кеширование используют вилку
                # проверяя есть ли значение в кэше и если есть,
                # то взять если нет то сохранить и взять
                # cache_value = cache.get('some_key')
                # if not cache_value:
                #     cache_value = "Cached value"
                #     cache.set('some_key', cache_value)

                students = Student.objects.all()

                context = {
                    "students": students,
                    'string': 'Test string',
                    # 'cached_value': cache_value,
                }

                return render(
                    request=request,
                    template_name="index.html",
                    context=context
                )
        else:
            return redirect(reverse('sign_in_view'))

class AddStudentByNameView(View):

    def get(self, request):

        student_name_from_request = request.GET.get('name')
        if not student_name_from_request:
            return HttpResponse('Student name missing')

        student = Student()
        student.name = student_name_from_request
        student.save()

        return HttpResponse('Student {} have been created'.format(student.name))

class AddNewStudentView(CreateView):

    # def get(self, request):
    #
    #     student_form = StudentForm()
    #     context = {
    #         'form': student_form,
    #     }
    #
    #     return render(
    #         request=request,
    #         template_name='student_form.html',
    #         context=context
    #     )
    #
    # def post(self, request):
    #
    #     student_form = StudentForm(request.POST)
    #     if student_form.is_valid():
    #         student_form.save()
    #
    #     return redirect(reverse('class_student_list'))

    model = Student
    fields = ['name', 'surname', 'age', 'gender', 'email', 'picture']
    template_name = 'student_form.html'
    success_url = reverse_lazy('class_student_list')

class DeleteStudentView(View):

    def get(self, request):

        student_id = request.GET.get('id')
        if not student_id:
            return HttpResponse('Missing student id')
        student = Student.objects.get(id=student_id)
        student.delete()

        return redirect(reverse('class_student_list'))

class UpdateStudentView(UpdateView):

    model = Student
    fields = ["name", "surname", "age", "gender", "email", "picture"]
    template_name = 'student_update.html'
    success_url = reverse_lazy('class_student_list')

class ShowBookView(ListView):

    model = Book
    template_name = 'book_list.html'

class BookDeleteView(View):

    def get(self, request):

        book_id = request.GET.get('id')
        if not book_id:
            return HttpResponse('Missing book id')
        book = Book.objects.get(id=book_id)
        book.delete()

        return redirect(reverse('class_books_list'))

class BookUpdateView(UpdateView):

    model = Book
    fields = ['title']
    template_name = 'book_update.html'
    success_url = reverse_lazy('class_books_list')

class ShowSubjectView(ListView):

    model = Subject
    template_name = 'subject_list.html'

class SubjectDeleteView(View):

    def get(self, request):

        subject_id = request.GET.get('id')
        if not subject_id:
            return HttpResponse('Missing subject id')
        subject = Subject.objects.get(id=subject_id)
        subject.delete()

        return redirect(reverse('class_subjects_list'))

class SubjectUpdateView(View):

    def get(self, request, id):

        subject = get_object_or_404(Subject, id=id)
        subject_form = SubjectForm(instance=subject)
        context = {
            'form': subject_form,
            'subject': subject,
        }

        return render(
            request = request,
            template_name = 'subject_update.html',
            context = context
        )
    def post(self, request, id):

        subject = get_object_or_404(Subject, id=id)
        subject_form = SubjectForm(request.POST, instance=subject)
        if subject_form.is_valid():
            subject_form.save()

        return redirect(reverse('class_subjects_list'))

class DeleteStudentFromSubjectView(View):
    def get(self,request):

        student_id = request.GET.get('id')
        student = Student.objects.get(id=student_id)
        subject_id = student.subject.id
        student.subject = None
        student.save()

        return redirect(reverse('class_subject_update', kwargs={'id': subject_id}), request_method = 'GET')

class AddStudentToSubjectView(View):

    def get(self, request, subject_id):

        student_id = request.GET.get('id')
        if not student_id:
            return HttpResponse('Missing student id')
        subject = get_object_or_404(Subject, id=subject_id)
        student = Student.objects.get(id=student_id)
        student.subject = subject
        student.save()

        return redirect(reverse('class_subject_update', kwargs={'id': subject_id}))

class ShowTeacherView(ListView):

    model = Teacher
    template_name = 'teacher_list.html'

class DeleteTeacherView(View):

    def get(self, request):

        teacher_id = request.GET.get('id')
        if not teacher_id:
            return HttpResponse('Missing teahcer ID')
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.delete()

        return redirect(reverse('class_teachers_list'))

class UpdateTeacherView(View):

    def get(self, request, id):

        teacher = get_object_or_404(Teacher, id=id)
        teacher_form = TeacherForm(instance=teacher)
        context = {
            'form': teacher_form,
            'teacher': teacher,
        }

        return render(
            request=request,
            template_name='teacher_update.html',
            context=context
        )

    def post(self, request, id):

        teacher = get_object_or_404(Teacher, id=id)
        teacher_form = TeacherForm(request.POST, instance=teacher)
        if teacher_form.is_valid():
            teacher_form.save()

        return redirect(reverse('class_teachers_list'))

class DeleteStudentFromTeacher(View):

    def get(self, request):

        student_id = request.GET.get('student_id')
        teacher_id = request.GET.get('teacher_id')
        student = Student.objects.get(id=student_id)
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.students.remove(student)

        return redirect(reverse('class_teacher_update', kwargs={'id': teacher_id}))

class AddStudentToTeacher(View):

    def post(self, request):

        teacher_id = request.POST.get('teacher_id')
        student_id = request.POST.get('student_id')
        if not student_id:
            return HttpResponse('Missing Stident ID')
        teacher = get_object_or_404(Teacher, id=teacher_id)
        student = Student.objects.get(id=student_id)
        teacher.students.add(student)

        return redirect(reverse('class_teacher_update', kwargs={'id': teacher_id}))

class SendMailview(View):

    def get(self, request):

        send_email(recipient_list = ['alfan2620@gmail.com',])

        return redirect(reverse('class_student_list'))

class CSVView(View):
    def get(self, request):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=data_students.csv"
        writer_for_response = csv.writer(response)
        writer_for_response.writerow(["Name", "Surname", "Subject", "Book"])

        students = Student.objects.all()
        for student in students:
            writer_for_response.writerow([
                student.name,
                student.surname,
                student.subject.title if student.subject else None,
                student.book.title if student.subject else None,
            ])

        return response

class JSONView(View):
    def get(self, request):

        student = Student.objects.first()
        students = Student.objects.all()

        return JsonResponse({
            "student": model_to_dict(student),
            "students": list(students.values(
                "name",
                "surname",
                "age",
                "gender",
                "subject__title",
                "book__title",
            )),
        })

class FileView(View):
    def get(self, request):

        with open('pyproject.toml') as file:
            read_file = file.read()

            response = FileResponse(read_file)
            response['Content-Disposition'] = "attachment; filename={}".format(file.name)

            return response
class XMLView(View):
    def get(self, request):
        with open('test_xml.xml') as file:
            read_file = file.read()
            response = FileResponse(read_file)
            response['Content-Type'] = 'text/xml'

            return response

class StudentAPIView(View):

    def get(self, request):

        students = Student.objects.all()

        return JsonResponse({
            'students': list(students.values(
                'id', 'name', 'surname', 'age', 'gender', 'email'
            ))
        })

# class StudentFilter(django_filters.FilterSet):
#
#     class Meta:
#         model = Student
#         fields = ('teachers__name',)

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    """
        filter_backends можно прописать здесь или же в settings для всех  и тогда просто для использования
         указывать по каким полям фильтровать,  при использовании filters.OrderingFilter аналогично
    """
    filterset_fields = ('name',)
    # filter_class = StudentFilter

    def create(self, request, *args, **kwargs):
        # Получаем данные из запроса
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Используем транзакцию для сохранения данных
        try:
            with transaction.atomic():
                # Создаем зачетку для студента
                new_book = Book.objects.create(title=uuid.uuid4())

                # Создаем студента и связываем с зачеткой
                student = Student.objects.create(
                    name=validated_data['name'],
                    surname=validated_data['surname'],
                    age=validated_data['age'],
                    gender=validated_data['gender'],
                    email=validated_data['email'],
                    # Другие поля студента
                    book=new_book
                )

                # Если все успешно, возвращаем статус 201 Created
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Если произошла ошибка, откатываем транзакцию
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def get_serializer(self):
    #     if self.request.method == 'GET':
    #         return ResponseStudentSerializer()
    #     else:
    #         return StudentSerializer()

    # def list(self, request, *args, **kwargs):
    #     students = Student.objects.all()
    #     student_serializer = StudentSerializer(instance=students, many=True)
    #     return Response(data={
    #         'students':student_serializer.data,
    #         'is_student':True
    #     }, status=status.HTTP_200_OK)
    # Переписан стандартный list

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('title',)

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('name',)

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('title',)

class CustomAPIViewSet(GenericViewSet):

    def list(self, request):

        utils.send_student_email()

        return Response({'status': 'OK'})


