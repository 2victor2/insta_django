FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app/