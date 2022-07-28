# syntax=docker/dockerfile:1
FROM python:3.9-alpine

WORKDIR /code

COPY . .

ENV FLASK_APP=fastgrad_api/app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers
RUN export SETUPTOOLS_USE_DISTUTILS=stdlib
RUN pip install -r requirements.txt
EXPOSE 5000

CMD flask run --reload

