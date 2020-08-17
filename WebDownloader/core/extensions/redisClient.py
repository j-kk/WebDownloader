from redis.client import Redis
from core.config import config

def set_redis():
    return Redis(config['REDIS_URL'], config['REDIS_PORT'], decode_responses=True)
