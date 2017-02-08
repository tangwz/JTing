# coding: utf-8
import ujson as json
from .base import ApiBlueprint, require_login
from jting.models import db, AdminRole, AdminUserRole

api = ApiBlueprint('roles')


@api.route('')
def list_roles():
    data = db.session.query(AdminRole).all()
    return json.dumps(dict(
        data=data
    )), 200


@api.route('', methods=['POST'])
def create_role():
    pass
