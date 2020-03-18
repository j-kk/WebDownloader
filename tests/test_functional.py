import os
import shutil
import time
import zipfile
from pathlib import Path

import pytest

from tests.fixtures import complete_app, module_schema, flask_app_client, custom_celery_worker


def test_environment(complete_app):
    """Test of the application environment."""
    assert complete_app.environment == 'testing'


def _run_test_text(flask_app_client, url, data_location, website_text_frazes):
    response = flask_app_client.open(method='POST', path='/getText', data=dict(url=url))
    assert response.status_code == 201
    task_id = response.data.decode().split('"')[-2]
    time.sleep(4)
    response = flask_app_client.open(method='GET', path='/downloadResult', data=dict(id=task_id))
    assert response.status_code == 200
    path = data_location.joinpath(Path(task_id + '.txt'))
    with open(path) as file:
        website = file.read()
        for item in website_text_frazes:
            assert item in website

def test_get_text01(flask_app_client, module_schema, custom_celery_worker):
    url = "https://www.mimuw.edu.pl/~noble/courses/MultivariateStatistics/"

    content_utterances = ["Course Information"]

    _run_test_text(flask_app_client, url, module_schema['DATA_LOCATION'], content_utterances)


def test_get_text02(flask_app_client, module_schema, custom_celery_worker):
    url = "https://www.mimuw.edu.pl/studia-lic-mgr"
    content_utterances = ["JSIM", "ubezpieczenie", " Koła studenckie "]
    _run_test_text(flask_app_client, url, module_schema['DATA_LOCATION'], content_utterances)



def _test_get_images_content(flask_app_client, url: str, data_location, content_images):
    response = flask_app_client.open(method='POST', path='/getImages', data=dict(url=url))
    assert response.status_code == 201
    task_id = response.data.decode().split('"')[-2]
    time.sleep(10)
    response = flask_app_client.open(method='GET', path='/downloadResult', data=dict(id=task_id))
    assert response.status_code == 200
    zip_path = data_location.joinpath(Path(task_id + '.zip'))

    with open(zip_path, 'wb') as file:
        file.write(response.data)

    dir_path = data_location.joinpath(task_id)
    dir_path.mkdir()
    shutil.unpack_archive(zip_path)
    if os.path.exists(dir_path):
        image_files_founded_for_url = os.listdir(dir_path)
        for image_file_name in content_images:
            assert image_file_name in image_files_founded_for_url


def test_get_images01(flask_app_client, module_schema, custom_celery_worker):
    url = "https://www.mimuw.edu.pl/"
    images_name = ["MIM_logo_sygnet_pl.png", "usos1.png"]
    _test_get_images_content(flask_app_client, url, module_schema['DATA_LOCATION'], images_name)


def test_get_images02(flask_app_client, module_schema, custom_celery_worker):
    url = "http://www.deltami.edu.pl/"
    images_name = ['01-kazana.tex-0-600_thumb_150px.png']
    _test_get_images_content(flask_app_client, url, module_schema['DATA_LOCATION'], images_name)

