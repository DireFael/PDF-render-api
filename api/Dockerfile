FROM python:3.8

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y poppler-utils
RUN pip install -r requirements.txt

