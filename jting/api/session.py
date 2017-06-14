# -*- coding: utf-8 -*-
from .base import ApiBlueprint
from jting.models import db, PyUser
from jting.config import DEFAULT_AVATAR
from jting.schema import PYUSER_SCHEMA, safe_validate
from jting.libs.token import encode_auth_token, decode_auth_token
from jting.libs.errors import SchemaError, APIException, NotConfidence
from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

api = ApiBlueprint('session')


@api.route('/new', methods=['POST'])
def register():
    data = request.get_json()
    account = data.get('account', None)
    password = data.get('password', None)
    nickname = data.get('nickname', None)

    if not safe_validate(data, PYUSER_SCHEMA):
        raise SchemaError()

    record = db.session.query(PyUser.account).filter_by(account=account).first()
    if record:
        return APIException(error='register failed.', description='account has been existed.')

    user = PyUser(
        account=account,
        password=generate_password_hash(password),
        nickname=nickname,
        avatar=DEFAULT_AVATAR,
    )
    with db.auto_commit():
        db.session.add(user)
        db.session.flush()

    request._token = encode_auth_token(user.id)

    return jsonify(
        account=account,
        nickname=nickname,
    ), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account', None)
    raw = data.get('password', None)

    record = db.session.query(PyUser.id, PyUser.nickname, PyUser.password, PyUser.role).filter_by(account=account).first()
    if not record:
        return APIException(error='login failed', description='No user.')

    uid, nickname, password, role = record
    if not check_password_hash(password, raw):
        return APIException(error='login failed', description='Invalid account or password.')

    if role >= 2:
        request._token = encode_auth_token(uid, True)
    else:
        request._token = encode_auth_token(uid)
    session['logined'] = True

    return jsonify(
        account=account,
        nickname=nickname
    ), 200


@api.route('/', methods=['DELETE'])
def logout():
    auth_token = request.headers.get('Authorization', None)
    if not auth_token:
        raise NotConfidence()
    suc, _ = decode_auth_token(auth_token)
    if not suc:
        raise NotConfidence()

    sid = session.pop('logined', None)
    if not sid:
        raise APIException(error='logout failed', description='session error.')
    return '', 204
