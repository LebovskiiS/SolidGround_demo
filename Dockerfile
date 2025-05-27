FROM python:3.12


RUN apt-get update && apt-get install -y libpq-dev gcc


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py collectstatic --noinput


EXPOSE 8000


CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "DjangoProject.asgi:application"]