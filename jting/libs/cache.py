# -*- coding: utf-8 -*-

from jting.config import REDIS_URI
from redis import StrictRedis

redis = StrictRedis.from_url(REDIS_URI)


