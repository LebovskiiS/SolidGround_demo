FROM python:3.12

RUN apt-get update && apt-get install -y libpq-dev gcc curl

WORKDIR /app

COPY . /app

RUN curl -L https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /usr/local/bin/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh


RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py collectstatic --noinput


EXPOSE 8000


CMD ["sh", "-c", "wait-for-it.sh db:5432 --timeout=60 --strict && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 DjangoProject.asgi:application"]