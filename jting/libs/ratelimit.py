# -*- coding: utf-8 -*-

import time
from flask import request
from functools import wraps
from .cache import redis
from .errors import LimitExceeded


class RateLimit(object):
    """Rate Limiting Decorator with Redis

    :param db:
    :param key:
    :param limit:
    :param per:
    :param prefix:
    :param send_x_headers:
    """
    expiration_window = 10

    def __init__(self, db, prefix='rate-limit'):
        self.db = db
        self.prefix = prefix

    def __call__(self, key_name, limit=300, per=60 * 1):
        key = self.prefix + str(key_name)
        ttl = self.get_data(key)
        if ttl < 0:
            self.set_data(key, per, limit - 1)
            return limit - 1, int(time.time()) + per
        else:
            remaining = self.decr_data(key)
            return remaining, int(time.time()) + ttl

    def get_data(self, full_key):
        return self.db.ttl(full_key)

    def set_data(self, full_key, expires, limit):
        return self.db.setex(full_key, expires, limit)

    def decr_data(self, full_key):
        return self.db.decr(full_key)


rlimit = RateLimit(redis)


def ratelimit(limit=400, per=60,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            key = '/%s/%s' % (key_func(), scope_func())
            remaining, reset = rlimit(key, limit, per)
            request._limit, request._remaining, request._reset = limit, remaining, reset
            if remaining <= 0 and reset:
                description = 'Rate limit exceeded, retry in %i' % reset
                raise LimitExceeded(description=description)
            else:
                return f(*args, **kw)
        return wrapper
    return decorator
