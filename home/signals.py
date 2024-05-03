import re

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from gender_guesser.detector import Detector

from home.models import Student


@receiver(pre_save, sender=Student)
def pre_save_normalized_name(sender, instance, **kwargs):

    instance.normalized_name = re.sub('[^\w\s]|_', '', instance.name + instance.surname).lower()


@receiver(pre_save, sender=Student)
def pre_save_check_gender_with_name(sender, instance, **kwargs):

    detector = Detector()
    gender_localy = detector.get_gender(instance.name)
    if gender_localy == 'male' or gender_localy == 'mostly_male':
        instance.gender = 'M'
    elif gender_localy == 'female' or gender_localy == 'mostly_female':
        instance.gender = 'F'
    else:
        instance.gender = gender_localy
    # instance.gender = detector.get_gender(instance.name)


# @receiver(pre_delete, sender=Student)
# def pre_delete_cancel_delete(sender, instance, **kwargs):
#     # Добавьте здесь вашу логику проверок перед удалением
#     # Если вы хотите отменить удаление, вызовите исключение или измените состояние объекта
#
#
#     should_cancel = input('Do you want to delete {}, write yes or not: '.format(instance))  # Замените на вашу логику проверки
#     if should_cancel.lower() == 'not':
#         print(f"Deletion of Student {instance} is canceled.")
#         # Вы можете вызвать исключение или изменить состояние объекта, чтобы отменить удаление
#         raise Exception("Deletion is canceled.")
#     else:
#         print('Students has been deleted')