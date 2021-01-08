FROM python:3.8.6-slim-buster
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /code
WORKDIR /code
