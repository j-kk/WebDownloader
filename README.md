## WebDownloader

Tool for downloading text & images from websites made with Flask & celery

### Installation

There are two ways to use this package - manual or docker. To install, simply type:

```
    pip install .
```

### Usage

It's recommended to run the app using docker, however for development purposes, it may be a bit painfull.

Firstly, you need redis server to enqueue tasks and save their state. You can do it with
```
    docker run -d -p 6379:6379 redis
```

To start the flask application, you can use the run.py script:

```
    python run.py
```

All the configuration should be specified in .env files (Just modify values from example.env and load the env file before launching with ```source```).
Assuming redis is working, you can start celery workers:

```
    celery -A WebDownloader.jobs.celery worker --loglevel=INFO
```

### Usage with Docker-compose

In order to start the whole system easily, we can use docker-compose :
```
    docker-compose up
```

It will start three docker containers :

- Redis
- Flask API
- Celery Worker
