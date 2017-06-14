# coding: utf-8

import os

APP_NAME = 'jting'
LOG_PATH = './test.log'

# config of flask app
SECRET_KEY = 'development'
SITE_MANIFEST = os.path.abspath('./manifest.json')

# config of mysql SQLAlchemy
SQLALCHEMY_NATIVE_UNICODE = False
SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_TRACK_MODIFICATIONS = True

# config of redis
REDIS_URI = ''

# DEFAULT AVATAR
DEFAULT_AVATAR = ''
