# -*- coding: utf-8 -*-
import jwt
import datetime
from flask import request
from jting.config import SECRET_KEY
from jting.logservice import logger
from jting.libs.errors import ServerError


def encode_auth_token(user_id, admin=False):
    """
    Generates the Auth Token
    :param user_id: user unique id
    :return: string
    """
    try:
        payload = {
            'sub': user_id,
            'exp': datetime.datetime.now() + datetime.timedelta(days=0, seconds=5),
            'admin': admin
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        logger.error(e)
        raise ServerError()


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token: jwt
    :return: integer or string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'
