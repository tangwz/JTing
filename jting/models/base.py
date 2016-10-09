# coding: utf-8

from contextlib import contextmanager

from flask import current_app, abort
from sqlalchemy.orm import Query, class_mapper
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

from jting.libs.cache import ONE_DAY, FIVE_MINUTES

__all__ = ['db', 'Base']

CACHE_TIMES = {
    'get': ONE_DAY,
    'count': ONE_DAY,
    'ff': FIVE_MINUTES,
    'fc': FIVE_MINUTES,
}
CACHE_MODEL_PREFIX = 'db'

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e

class CacheProperty(object):
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = class_mapper(type)
            if mapper:
                return CacheProperty(mapper, session=self.sa.session())
        # TODO: add UnmappedclassError
        except:
            return None

class BaseMixin(object):
    def __getitem__(self, key):
        return getattr(self, key)

db = SQLAlchemy(session_options={
    'expire_on_commit': False,
    'autoflush': False,
})

class Base(db.Model, BaseMixin):
    __abstract__ = True
    cache = CacheProperty(db)