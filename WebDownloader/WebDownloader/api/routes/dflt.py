from flask import Blueprint

health = Blueprint('health', __name__)


@health.route('/', methods=['GET'])
def mget():
    return "", 200