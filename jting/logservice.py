# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, DatagramHandler
from config import APP_NAME, LOG_PATH


def getHandler(name, **kwargs):
    file_path = kwargs.get('file_path')

    if name == 'FileHandler':
        return logging.FileHandler(file_path)
    elif name == 'RotatingFileHandler':
        return RotatingFileHandler(file_path, maxBytes=100*1024*1024, backupCount=10)
    elif name == 'TimedRotatingFileHandler':
        return TimedRotatingFileHandler(file_path, when='midnight')
    elif name == 'DatagramHandler':
        return MyDatagramHandler(kwargs.get('host'), kwargs.get('port'))
    else:
        return logging.StreamHandler()


def getLogger(name, type, level, file_path=None):
    logger = logging.getLogger(name)

    handler = getHandler(type, file_path=file_path)
    handler.setFormatter(logging.Formatter(
        '%(name)-4s %(asctime)s %(funcName)s %(lineno)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S'))

    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = getLogger(APP_NAME, 'RotatingFileHandler', logging.DEBUG, LOG_PATH)


class MyDatagramHandler(DatagramHandler):
    infolist = ['process','created','filename','lineno','msg','funcName',]
    def makePickle(self,record):
        record.__dict__['msg'] = record.getMessage()
        s = "%(name)s,,%(filename)s,,%(funcName)s,,%(process)s,,%(lineno)s,,%(msg)s" % record.__dict__
        return s.encode("utf8","replace") if isinstance(s,unicode) else s
