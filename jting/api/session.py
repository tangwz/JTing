# -*- coding: utf-8 -*-
from .base import ApiBlueprint
from jting.forms import RegisterForm, LoginForm
from jting.libs.token import encode_auth_token, decode_auth_token
from jting.libs.errors import APIException, NotConfidence, FormError
from flask import request, jsonify, session

api = ApiBlueprint('session')


@api.route('/new', methods=['POST'])
def register():
    form = RegisterForm.create_api_form()
    user = form.create_user()

    request._token = encode_auth_token(user.id)

    return jsonify(
        account=user.account,
        nickname=user.nickname,
    ), 201


@api.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        raise FormError(form)

    user = form.user
    if user.role >= 2:
        print 'xxx'
        request._token = encode_auth_token(user.id, True)
    else:
        request._token = encode_auth_token(user.id)
    session['logined'] = True

    return jsonify(
        account=user.account,
        nickname=user.nickname
    ), 200


@api.route('/', methods=['DELETE'])
def logout():
    Authorization = request.headers.get('Authorization', None)
    auth_token = Authorization.split(' ')[-1]
    if not auth_token:
        raise NotConfidence()
    suc, _ = decode_auth_token(auth_token)
    if not suc:
        raise NotConfidence()

    sid = session.pop('logined', None)
    if not sid:
        raise APIException(error='logout failed', description='You have been logout.')
    return '', 204
