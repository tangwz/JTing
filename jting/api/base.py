# coding: utf-8

from functools import wraps
from flask import request, session
from jting.libs.errors import NotAuth, NotConfidential


class ApiBlueprint(object):
    def __init__(self, name):
        self.name = name
        self.deferred = []

    def route(self, rule, **options):
        def wrapper(f):
            self.deferred.append((f, rule, options))
            return f
        return wrapper

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name

        for f, rule, options in self.deferred:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)


def require_login(permission=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logined', False):
                raise NotAuth()

            return f(*args, **kwargs)

        return decorated
    return wrapper
