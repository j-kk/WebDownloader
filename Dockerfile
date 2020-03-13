FROM python:3.7
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/
COPY . /app

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

ENV APP_ENVIRONMENT development
ENV FLASK_APP app
ENV FLASK_DEBUG True

WORKDIR /app