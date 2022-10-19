# syntax=docker/dockerfile:1
FROM python:3.9-alpine

WORKDIR /app

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV SETUPTOOLS_USE_DISTUTILS=stdlib

RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app/fastgrad_api
CMD gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:app
