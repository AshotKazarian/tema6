# Основа образа - Python 3.8
FROM python:3.8

RUN pip install --upgrade pip

# Установка необходимых пакетов
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Создание директории для проекта
WORKDIR  app

# Копирование файлов проекта в контейнер
COPY . /app

# Установка зависимостей Django
RUN python manage.py migrate

# Запуск Django сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]