from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html

from home.models import Student


# Register your models here.

class StudentAdmin(ModelAdmin):
    # Список полей который нужно отображать на таблице-списке модели
    list_display = ('id', 'custom_field', 'email', 'birthday')
    # Список полей по которым можно в админке фильтровать таблицу
    list_filter = ('id',)
    # Список полей по которым будет происходить поиск в админке
    search_fields = ('id', 'email',)
    # Список полей по которым будет происходить сортировка в админке для данной таблицы
    ordering = ('id', 'birthday',)
    # Поля которые должны быть только чтение на странице редактирования записи
    readonly_fields = ('id',)

    def custom_field(self, instance):
        """
        Кастомное поле, то поле которого нет в модели но нужно отобразить на таблице-списке
        данных текущей модели,
        Данный метод принимает объект той модели которой мы привизали в admin.site.register
        """
        if instance.social_url:
            return format_html("<a href='{}'>{}{}</a>",
                            instance.social_url,
                            instance.name,
                            instance.surname,
                            )


admin.site.register(Student, StudentAdmin)