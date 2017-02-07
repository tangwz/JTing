# coding: utf-8
import base64
from flask import request, current_app, url_for
from flask import copy_current_request_context
from werkzeug._compat import to_bytes, to_unicode
try:
    import gevent
except ImportError:
    gevent = None


def run_task(func, *args, **kwargs):
    if gevent and current_app.config.get('JTING_ASYNC'):
        gevent.spawn(copy_current_request_context(func), *args, **kwargs)
    else:
        func(*args, **kwargs)


def xmldatetime(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def build_url(baseurl, endpoint, **kwargs):
    if baseurl:
        baseurl = baseurl.rstrip('/')
        urlpath = url_for(endpoint, **kwargs)
        return '%s%s' % (baseurl, urlpath)
    kwargs['_external'] = True
    return url_for(endpoint, **kwargs)


def full_url(endpoint, **kwargs):
    baseurl = current_app.config.get('SITE_URL')
    return build_url(baseurl, endpoint, **kwargs)


def decode_base64(text, encoding='utf-8'):
    text = to_bytes(text, encoding)
    return to_unicode(base64.b64decode(text), encoding)


class Pagination(object):
    def __init__(self, total, page=1, perpage=20):
        self.total = total
        self.page = page
        self.perpage = perpage

        pages = int((total - 1) / perpage) + 1
        self.pages = pages

        if page > 1:
            self.prev = page - 1
        else:
            self.prev = None
        if page < pages:
            self.next = page + 1
        else:
            self.next = None

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return ['total', 'page', 'perpage', 'prev', 'next', 'pages']

    def fetch(self, q):
        offset = (self.page - 1) * self.perpage
        if offset:
            q = q.offset(offset)
        return q.limit(self.perpage).all()


class Empty(object):
    def __eq__(self, other):
        return isinstance(other, Empty)

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    def __str__(self):
        return "Empty"

    def __repr__(self):
        return '<Empty>'

EMPTY = Empty()