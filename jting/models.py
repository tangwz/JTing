# coding: utf-8
from logservice import logger
from config import SQLALCHEMY_DATABASE_URI
from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=5, pool_recycle=300, max_overflow=3, echo=False)
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

    def __del__(self):
        self.close()

    def close(self):
        self.session.remove()


db = Session()


Base = declarative_base()


class PyUser(Base):
    __table__ = Table('py_user', metadata, autoload=True)
