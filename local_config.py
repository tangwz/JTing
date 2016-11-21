# coding: utf-8
"""
    jting.local_config
    ~~~~~~~~~~~~~~~~~~~~

    This local config just used in local environment.
"""

import os

SECRET_KEY = 'development'
SQLALCHEMY_NATIVE_UNICODE = False
SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_TRACK_MODIFICATIONS = True
JTING_REDIS_URI = ''
JTING_CACHE_REDIS_URI = ''

DEBUG = True
SITE_MANIFEST = os.path.abspath('./manifest.json')