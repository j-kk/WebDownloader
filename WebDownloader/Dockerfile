FROM python:3.8 AS wd_python
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

COPY requirements.txt /tmp/

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN pip3 install gunicorn


COPY . /app
WORKDIR /app


