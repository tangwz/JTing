# coding: utf-8

from flask import request
from .errors import APIException
from jting.models import db


class Pagination(object):
    def __init__(self, total, page=1, per_page=20):
        self.total = total
        self.page = page
        self.per_page = per_page

        pages = int((total - 1) / per_page) + 1
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
        return ['total', 'page', 'per_page', 'pages', 'prev', 'next']

    def fetch(self, q):
        offset = (self.page - 1) * self.per_page
        if offset:
            q = q.offset(offset)
        return q.limit(self.per_page).all()


def int_or_raise(key, value=0, maxvalue=None):
    try:
        num = int(request.args.get(key, value))
        if maxvalue is not None and num > maxvalue:
            return maxvalue
        return num
    except ValueError:
        raise APIException(description='Require int type on %s parameter' % key)


def get_pagination_query():
    page = int_or_raise('page', 1)
    if page < 1:
        raise APIException(description='page should be larger than 1')

    per_page = int_or_raise('perpage', 10, 100)
    if per_page < 10:
        raise APIException(description='per page should be larger than 10')

    return page, per_page


def pagination_query(model, key, **filters):
    page, per_page = get_pagination_query()

    total = db.session.query(model).filter_by(**filters).count()
    rv = Pagination(total, page, per_page)

    if page > rv.pages:
        raise APIException(description='page should be smaller than total pages')

    if not isinstance(key, str):
        q = db.session.query(model).filter_by(**filters).order_by(key)
        return rv.fetch(q), rv

    order_key = request.args.get('key', key)
    desc = request.args.get('order') != 'asc'
    if not hasattr(model, order_key):
        order_key = key

    field = getattr(model, order_key)
    if desc:
        field = field.desc()

    q = db.session.query(model).filter_by(**filters).order_by(field)
    data = rv.fetch(q)
    return data, rv
