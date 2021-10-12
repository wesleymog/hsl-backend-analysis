# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY *.py ./

EXPOSE 3000
CMD exec gunicorn --worker-class eventlet --workers 1 --bind :3000 wsgi:app

