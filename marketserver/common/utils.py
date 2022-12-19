import json
import logging
import threading
from common import conf


class SingletonType(type):
    
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if hasattr(cls, "_instance"):
            return cls._instance
        with SingletonType._instance_lock:
            if not hasattr(cls, "_instance"):
                cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance

def loadRequest(data):
    req = {}
    try:
        req = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        logging.error("loadRequest invalid "
            "request: {}".format(data))
        return conf.ERR_INVALID_REQUEST, req
    return 0, req