# coding: utf-8
import ujson as json
from .base import ApiBlueprint, require_login
from jting.forms import UserForm
from jting.models import db, AdminUser

api = ApiBlueprint('users')


@api.route('')
@require_login(permission=None)
def list_users():
    q = db.session.query(AdminUser)
    data = q.limit(20).all()
    return json.dumps(dict(data=data)), 200


@api.route('', methods=['POST'])
def create_user():
    form = UserForm.create_api_form()
    user = form.create_user()
    return json.dumps(dict(
        data=user
    )), 201
