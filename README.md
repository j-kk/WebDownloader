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

All the configuration should be specified in .env files (Just modify values from example.env and load the env file before launching with ```source & export DATA_LOCATION```).
Assuming redis is working, you can start celery workers:

```
    celery -A WebDownloader.jobs.worker.celery worker --loglevel=INFO
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

### API

The RESTful API offers 4 methods:

- `/getText?url=example.com` - downloads all text from website and returns taskID
- `/getImages?url=example.com` - downloads all images from website and returns taskID
- `/checkState?id=1234` - returns task state
- `/downloadResult?id=1234` - returns task result

### TODOs

- Celery doesn't distinguish between pending and not existing tasks - add 'after_send' handler
- Improve imageTask to download images concurrently
- Unify tests with some class etc
- fixture redis 

### Comment

In my honest opinion, it was quite a big recruitment task. It wasn't difficult, but it required some knowledge
in celery (which was new to me) & flask (which I know a bit). I had to study it a bit, what cost me a bit of time 
(which is preciouse duries studies, especially remote :/ ). If I had more time, I would:
- fix test_functional unzipping - because it works, but shutil.unpack_archive has standarization dilemma
- Unify tests in some classes
- do TODOs ;p
- and clearify the code ;)
