from time import sleep

import requests
from celery import shared_task, chain, group, chord

from home.models import Student, Currency


@shared_task(bind=True, name='celery_test2')
def test_task_celery2(self):
    sleep(3)
    print('Celery Test2')
    return 'Request: {}'.format(self)



@shared_task(name='celery_test3')
def sum_number(*args):
    return sum(args)

@shared_task(name='celery_test_chain')
def compile_task():
    chain(
        sum_number.si(1,3), #chain используется для выполнения тасков асинхронно, но последоатльно
        sum_number.s(4)
    )()

@shared_task(name='celery_test_group')
def group_numbers():
    # выполнение всех тасков паралельно
    return group([
        sum_number.s(1, 2),
        sum_number.s(3, 4)
    ])()
@shared_task
def chord_numbers():
    # выполнение всех тасков паралельно, но после того как все выполнится выполнить sum_task
    return chord([
        sum_number.s(1, 2),
        sum_number.s(3, 4)])\
        (sum_task.si())

@shared_task
def sum_task(*args):
    return args

@shared_task(name='take_model_instance')
def student_show(student_id):
    student = Student.objects.get(id=student_id)
    print(student)
    return True

@shared_task(name='take_date_from_Privat')
def take_data():
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    return response.json()

@shared_task(name='save_data_to_currency')
def save_data_to_currency(response):
    for i in response:
        currency = Currency()
        currency.ccy = i['ccy']
        currency.buy = i['buy']
        currency.sale = i['sale']
        currency.save()
    return True
@shared_task()
def night_and_morning():
    chain(
        take_data.si(),
        save_data_to_currency.s()
    )()

