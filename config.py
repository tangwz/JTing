# coding: utf-8

import os

SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'mysql://jting:jting@192.168.42.128/dev'
JTING_REDIS_URI = ''
JTING_CACHE_REDIS_URI = ''

DEBUG = True
SITE_MANIFEST = os.path.abspath('./manifest.json')