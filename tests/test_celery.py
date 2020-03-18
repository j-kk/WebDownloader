import time
from pathlib import Path


def test_celery_text_task01(complete_app, custom_celery_worker):
    url = "https://www.mimuw.edu.pl/~noble/courses/MultivariateStatistics/"
    content_utterances = ["Multivariate Statistics",
                          " Asymptotic log likelihood ratio tests; Wald, Rao, Pearson; logistic regression."]
    result_id = complete_app.celeryClient.textTask.delay(url).id
    time.sleep(2.5)
    assert complete_app.celeryClient.check_state(result_id) == 'SUCCESS'

    file_name = complete_app.celeryClient.find_result(result_id)

    path = complete_app['DATA_LOCATION'].joinpath(Path(file_name))
    assert path.is_file()

    with open(path, 'r') as file:
        file_content = file.read()
        for item in content_utterances:
            assert item in file_content

    path.unlink()


def test_celery_images(complete_app, custom_celery_worker):
    url = "https://google.com/"
    result_id = complete_app.celeryClient.imageTask.delay(url).id
    time.sleep(5)
    assert complete_app.celeryClient.check_state(result_id) == 'SUCCESS'

    file_name = complete_app.celeryClient.find_result(result_id)

    path = complete_app['DATA_LOCATION'].joinpath(Path(file_name))
    assert path.is_file()
    path.unlink()


def test_celery_text_task02(complete_app, custom_celery_worker):
    url = "https://www.naguiobgiabgiouabiofgbao.pl"
    result_id = complete_app.celeryClient.textTask.delay(url).id
    time.sleep(1)
    assert complete_app.celeryClient.check_state(result_id) == 'FAILURE'
