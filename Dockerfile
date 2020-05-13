FROM python:3.7
MAINTAINER Suvigya Agrawal

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

WORKDIR /src
COPY . /src
