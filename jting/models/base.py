# coding: utf-8

from contextlib import contextmanager

from flask import current_app, abort
from sqlalchemy import event, func
from sqlalchemy.orm import Query, class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

from jting.libs.cache import cache, ONE_DAY, FIVE_MINUTES

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

db = SQLAlchemy(session_options={
    'expire_on_commit': False,
    'autoflush': False,
})

class CacheQuery(Query):
    """
    Subclass of Query aim to query cache firstly.
    """
    def get(self, ident):
        mapper = self._only_full_mapper_zero('get')

        if isinstance(ident, (list, tuple)):
            suffix = '-'.join(map(str, ident))
        else:
            suffix = str(ident)

        key = mapper.class_.generate_cache_prefix('get') + suffix
        rv = cache.get(key)
        if rv:
            return rv

        rv = super(CacheQuery, self).get(ident)
        if rv is None:
            return None
        cache.set(key, rv, CACHE_TIMES['get'])
        return rv

    def get_dict(self, idents):
        if not idents:
            return {}

        mapper = self._only_full_mapper_zero('get')
        if len(mapper.primary_key) != 1:
            raise NotImplementedError

        prefix = mapper. class_.generate_cache_prefix('get')
        keys = {prefix + str(i) for i in idents}
        rv = cache.get_dict(*keys)

        missed = {i for i in idents if rv[prefix + str(i)] is None}

        rv = {k.lstrip(prefix): rv[k] for k in rv}

        if not missed:
            return rv

        pk = mapper.primary_key[0]
        missing = self.filter(pk.in_(missed)).all()
        to_cache = {}
        for item in missing:
            ident = str(getattr(item, pk.name))
            to_cache[prefix + ident] = item
            rv[ident] = item

        cache.set_many(to_cache, CACHE_TIMES['get'])
        return rv

    def get_many(self, idents, clean=True):
        d = self.get_dict(idents)
        if clean:
            return list(_itervalues(d, idents))
        return [d[str(k)] for k in idents]


class CacheProperty(object):
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = class_mapper(type)
            if mapper:
                return CacheQuery(mapper, session=self.sa.session())
        # TODO: add UnmappedclassError
        except UnmappedClassError:
            return None

class BaseMixin(object):
    def __getitem__(self, key):
        return getattr(self, key)

    @classmethod
    def generate_cache_prefix(cls, name):
        prefix = '%s:%s:%s' % (CACHE_MODEL_PREFIX, name, cls.__tablename__)
        if hasattr(cls, '__cache_version__'):
            return '%s|%s:' % (prefix, cls.__cache_version__)
        return '%s:' % prefix

    @classmethod
    def __declare_last__(cls):
        @event.listens_for(cls, 'after_insert')
        def receive_after_insert(mapper, conn, target):
            cache.inc(target.generate_cache_prefix('count'))

        @event.listens_for(cls, 'after_update')
        def receive_after_update(mapper, conn, target):
            key = _unique_key(target, mapper.primary_key)
            cache.set(key, target, CACHE_TIMES['get'])

        @event.listens_for(cls, 'after_delete')
        def receive_after_delete(mapper, conn, target):
            key = _unique_key(target, mapper.primary_key)
            cache.delete_many(key, target.generate_cache_prefix('count'))

class Base(db.Model, BaseMixin):
    __abstract__ = True
    cache = CacheProperty(db)


def _unique_suffix(target, primary_key):
    return '-'.join(map(lambda k: str(getattr(target, k.name)), primary_key))

def _unique_key(target, primary_key):
    key = _unique_suffix(target, primary_key)
    return target.generate_cache_prefix('get') + key

def _itervalues(data, idents):
    for k in idents:
        item = data[str(k)]
        if item is not None:
            yield item