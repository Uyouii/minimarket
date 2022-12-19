import json
import logging
import redis
from common import conf
from common import utils


class RedisCache:

    __metaclass__ = utils.SingletonType

    def __init__(self):
        pool = redis.ConnectionPool(
            host='localhost', port=6379,
            decode_responses=True, db=conf.REDIS_DB_ID
        )

        self.db = redis.Redis(connection_pool=pool)

    def set(self, key, value, timeout=None):
        logging.info("RedisCache, set to cache: {}".format(key))
        if not isinstance(value, str):
            value = json.dumps(value)
        self.db.set(key, value, ex=timeout)

    def get(self, key):
        logging.info("RedisCache, get from cache: {}".format(key))
        data = self.db.get(key)
        return json.loads(data) if data else None
    
    def delete(self, key):
        logging.info("RedisCache, delete from cache: {}".format(key))
        self.db.delete(key)
