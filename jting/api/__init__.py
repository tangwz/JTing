# coding: utf-8
import re
from flask import Blueprint, request
from . import  session


VERSION_URL = re.compile(r'^/api/v\d/')
VERSION_ACCEPT = re.compile(r'application/vnd\.jting\+json;\s+version=(\d)')
CURRENT_VERSION = '1'


bp = Blueprint('api', __name__)


@bp.after_request
def headers_hook(response):
    if request.method == 'GET':
        response.headers['Access-Control-Allow-Origin'] = '*'

    # set jwt authorization header
    token = getattr(request, '_token', None)
    if token:
        response.headers['Authorization'] = 'Bearer ' + token

    # You can check the returned HTTP headers of API request
    # to see your current rate limit status
    limit = getattr(request, '_limit', None)
    remaining = getattr(request, '_remaining', None)
    reset = getattr(request, '_reset', None)

    if limit:
        response.headers['X-RateLimit-Limit'] = limit
    if remaining:
        response.headers['X-RateLimit-Remaining'] = remaining
    if reset:
        response.headers['X-RateLimit-Reset'] = reset

    # api not available in iframe
    response.headers['X-Frame-Options'] = 'deny'
    # security protection
    response.headers['Content-Security-Policy'] = "default-src 'none'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


def find_version(environ):
    accept = environ.get('HTTP_ACCEPT')
    if not accept:
        return CURRENT_VERSION
    rv = VERSION_ACCEPT.findall(accept)
    if rv:
        return rv[0]
    return CURRENT_VERSION


class ApiVersionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if not path.startswith('/api/'):
            return self.app(environ, start_response)
        if VERSION_URL.match(path):
            return self.app(environ, start_response)

        # supported a default version: current version
        version = find_version(environ)
        environ['PATH_INFO'] = path.replace('/api/', '/api/v%s' % version)
        return self.app(environ, start_response)


def init_app(app):
    app.wsgi_app = ApiVersionMiddleware(app.wsgi_app)

    session.api.register(bp)

    app.register_blueprint(bp, url_prefix='/api/v' + str(CURRENT_VERSION))
