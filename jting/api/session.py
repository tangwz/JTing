# coding: utf-8

import ujson as json
from flask import session, request
from jting.models import db, AdminUser
from werkzeug.security import check_password_hash
from .base import ApiBlueprint
from jting.libs.utils import decode_base64

api = ApiBlueprint('session')


@api.route('', methods=['POST', 'DELETE'])
def login_session():
    if request.method == 'DELETE':
        session.pop('logined', None)
        session.pop('username', None)
        return '', 204

    if request.mimetype == 'application/json':
        username, password = parse_auth_headers()
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)

    if not username or not password:
        return json.dumps(dict(
            error='username or password are required.'
        )), 400

    user = db.session.query(AdminUser).filter(AdminUser.username == username.lower()).first()
    if not user or check_password_hash(user.password, password):
        return json.dumps(dict(
            error='Invalid username or password.'
        )), 400

    session['logined'] = True
    session['username'] = username
    return json.dumps()


@api.route('/new', methods=['POST'])
def signup_session():
    # maybe the internel system do not need signup.
    return json.dumps(dict(
        error = 'the internel system do not need signup.'
    )), 400


def parse_auth_headers():
    data = request.headers.get('Authorization')
    if not data:
        return None, None
    data = data.replace('Basic ', '').strip()
    return decode_base64(data).split(':', 1)