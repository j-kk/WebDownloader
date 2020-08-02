import os
import threading

import pytest
from app.testing import FlaskClient

from WebDownloader.backend.api import TaskView
from WebDownloader.core.factory import Module

Module.environment = 'testing'


# TODO redis fixture

@pytest.yield_fixture(scope='session')
def module_schema():
    """Fixture of factory with testing environment."""
    os.environ['DATA_LOCATION'] = './WebDownloader'
    os.environ['APP_ENVIRONMENT'] = 'testing'  # create module

    yield Module(environment='testing')


@pytest.fixture(scope='session')
def celery_app(module_schema):
    module_schema.set_celery()
    return module_schema.celeryClient.celery


@pytest.fixture(scope='session')
def celery_config(module_schema):
    return {
        'broker_url': module_schema.config['BROKER_URL'],
        'result_backend': module_schema.config['BROKER_URL']
    }


@pytest.yield_fixture(scope='session')
def custom_celery_worker(module_schema):
    celery = module_schema.set_celery()
    from celery.bin import worker
    worker = worker.worker(app=celery)
    thread = threading.Thread(target=worker.run)
    thread.daemon = True
    thread.start()

    yield celery


@pytest.yield_fixture(scope='session')
def complete_app(module_schema):
    """Fixture of application creation."""
    module_schema.set_flask()
    module_schema.set_celery()
    # Create api view
    taskView = TaskView()
    # Register the backend blueprint
    module_schema.register_blueprint(taskView.createBlueprint(module_schema.flask, module_schema.celeryClient))
    yield module_schema


@pytest.fixture(scope='session')
def flask_app_client(complete_app):
    """Fixture of application client."""
    app = complete_app.flask
    app.config['TESTING'] = True
    app.config['DATA_LOCATION'] = complete_app['DATA_LOCATION']
    app.test_client_class = FlaskClient
    return app.test_client()
