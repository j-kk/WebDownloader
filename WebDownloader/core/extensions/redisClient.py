from redis.client import Redis
from WebDownloader.core.config import Config

def set_redis(config: Config):
    return Redis(config['REDIS_URL'], config['REDIS_PORT'], decode_responses=True)
