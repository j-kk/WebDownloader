FROM python:3.8 AS wd_python
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

COPY ../WebDownloader/requirements.txt /tmp/

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY requirements.txt /tmp/

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY ../WebDownloader /app/
COPY app.py /app
COPY API /app/
WORKDIR /app


