# -*- coding: utf-8 -*-
from flask import request
from .errors import NotConfidence
from .token import decode_auth_token


def jwt_auth():
    Authorization = request.headers.get('Authorization', None)
    auth_token = Authorization.split(' ')[-1]
    if not auth_token:
        raise NotConfidence()
    suc, data = decode_auth_token(auth_token)
    if not suc:
        raise NotConfidence()
    return data
