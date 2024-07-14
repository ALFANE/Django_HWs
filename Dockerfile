# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /usr/src/

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . .

# Устанавливаем Poetry для управления зависимостями
RUN pip install poetry

# Устанавливаем зависимости проекта с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install

# Собираем статические файлы (если нужно)
RUN poetry run python manage.py collectstatic --noinput

# Указываем, что контейнер прослушивает порт 8001
EXPOSE 8001

# Устанавливаем команду по умолчанию для запуска приложения на порту 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]