## WebDownloader

Tool for downloading text & images from websites made with Flask & celery

### Installation

There are two ways to use this package - manual or docker. To install, simply type:

```
    pip install .
```

### Usage

It's recommended to run the app using docker, however for development purposes, it may be a bit painfull.

To start the application, you can use the run.py script:

```
    python run.py
```

However, for correct work Redis server is needed. Configuration should be specified in .env files.
Assuming redis is working, you can start celery workers:

```
    celery -A app.jobs.celery worker --loglevel=INFO
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
