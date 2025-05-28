FROM python:3.12

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y libpq-dev gcc curl

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем весь проект в контейнер
COPY . /app

# Скачиваем и делаем wait-for-it.sh исполняемым
RUN curl -L https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /app/wait-for-it.sh && chmod +x /app/wait-for-it.sh

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Указываем открытый порт в контейнере
EXPOSE 8000

# Добавляем команду запуска с использованием wait-for-it.sh
CMD ["sh", "-c", "/app/wait-for-it.sh db:5432 --timeout=60 --strict && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 DjangoProject.asgi:application"]