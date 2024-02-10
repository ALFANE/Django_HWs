from time import sleep

from celery import shared_task, chain


@shared_task(bind=True, name='celery_test2')
def test_task_celery2(self):
    sleep(3)
    print('Celery Test2')
    return 'Request: {}'.format(self)

@shared_task(bind=True, name='celery_test3')
def app(self,a,b):
    return a + b

@shared_task(bind=True, name='celery_test_chain')
def compile_task(self):
    chain(
        app.si(1,3) #chain используется для выполнения тасков асинхронно, но последоатльно
        |
        app.si(3,3)
    )()
