import os
from time import sleep

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('Django', include=[])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, name='celery_test' """, queue='test'""")
def test_task_celery(self):
    sleep(3)
    print('Celery Test')
    return 'Request: {}'. format(self)



