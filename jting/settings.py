# coding: utf-8

"""
    jting.ettings
    ~~~~~~~~~~~~~~~~~~~~

    This is the jting's settings.

    description:
        Settings of specific database and config parameters.
"""

import datetime

SITE_NAME = 'JTING'
SITE_DESCRIPTION = 'JTing is a API-based platform.'
SITE_YEAR = datetime.date.today().year

# cache settings
JTING_CACHE_TYPE = 'redis'
JTING_CACHE_REDIS_DB = 2
JTING_REDIS_URI = ''