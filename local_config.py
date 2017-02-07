# coding: utf-8
"""
    jting.local_config
    ~~~~~~~~~~~~~~~~~~~~

    This local config just used in local environment.

    description:
        A global software and environment config.
"""

import os

# config of flask app -- jting
DEBUG = True
SECRET_KEY = 'development'
SITE_MANIFEST = os.path.abspath('./manifest.json')

# config of mysql SQLAlchemy
SQLALCHEMY_NATIVE_UNICODE = False
SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_TRACK_MODIFICATIONS = True

# config of redis
JTING_REDIS_URI = ''
JTING_CACHE_REDIS_URI = ''