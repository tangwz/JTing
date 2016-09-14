# coding: utf-8

from flask import request, current_app, url_for
from flask import copy_current_request_context
try:
    import gevent
except ImportError:
    gevent = None

def is_json():
    if request.is_xhr:
        return True

    if request.path.startswith('/api/'):
        return True

    if hasattr(request, 'oauth_client'):
        return True

    return False

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