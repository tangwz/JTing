# coding: utf-8
from logservice import logger
from config import SQLALCHEMY_DATABASE_URI
from contextlib import contextmanager
from jting.libs.errors import ServerError
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=5, pool_recycle=300, max_overflow=3, echo=True)
metadata = MetaData(bind=engine)


session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Session(object):
    def __init__(self, cls=session_factory):
        self.session = scoped_session(cls)

    @contextmanager
    def auto_commit(self, throw=False):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            if throw:
                raise e
            else:
                logger.error(e)
                raise ServerError(description='System error. Please contact to the admin.')

    def __del__(self):
        self.close()

    def close(self):
        self.session.remove()


db = Session()


Base = declarative_base()


class PyHub(Base):
    __table__ = Table('py_hub', metadata, autoload=True)

    @staticmethod
    def keys():
        return ('title', 'link', 'desc', 'user_id', 'status', 'addtime', 'views', 'replies', 'likes')

    def __getitem__(self, item):
        return getattr(self, item)


class PyComment(Base):
    __table__ = Table('py_comment', metadata, autoload=True)


class PyUser(Base):
    __table__ = Table('py_user', metadata, autoload=True)
