# Основа образа - Python 3.9
FROM python:3.9

RUN pip install --upgrade pip

# Установка необходимых пакетов
COPY requirements.txt /shop/
RUN pip install -r shop/requirements.txt

# Создание директории для проекта
WORKDIR  shop

# Копирование файлов проекта в контейнер
COPY . /shop

# Установка зависимостей Django
RUN python manage.py migrate

# Запуск Django сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
