# coding: utf-8
import ujson as json
from .base import ApiBlueprint, require_login
from jting.forms import UserForm
from jting.models import db, AdminUser
from jting.libs.errors import NotFound

api = ApiBlueprint('users')


@api.route('', methods=['GET'])
def list_users():
    q = db.session.query(AdminUser.username, AdminUser.email, AdminUser.name, AdminUser.phone)
    data = q.limit(20).all()
    return json.dumps(dict(data=data)), 200


@api.route('', methods=['POST'])
def create_user():
    form = UserForm.create_api_form()
    user = form.create_user()
    return json.dumps(dict(
        data=user
    )), 201


@api.route('/<username>', methods=['PATCH'])
def update_user(username):
    user = db.session.query(AdminUser).filter(
        AdminUser.username == username
    ).first()
    if not user:
        raise NotFound('no user called "%s"' % username)
    form = UserForm.create_api_form(obj=user)
    user = form.update_user(user)
    return json.dumps(user)


@api.route('/<username>', methods=['DELETE'])
def delete_user(username):
    user = db.session.query(AdminUser).filter(
        AdminUser.username == username
    ).first()
    if not user:
        raise NotFound('no user called "%s"' % username)
    with db.auto_commit():
        db.session.query(AdminUser).filter(AdminUser.username == username).delete()
    return json.dumps(user)
