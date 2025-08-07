FROM python:3

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/ ./app/
COPY requirements.txt .
COPY .env .

RUN pip install -r requirements.txt