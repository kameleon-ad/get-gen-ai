FROM python:3.10.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y gcc libpq-dev postgresql

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
