# coding: utf-8
import ujson as json
from .base import ApiBlueprint, require_login
from jting.forms import RoleForm
from jting.libs.errors import NotFound
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
    form = RoleForm.create_api_form()
    role = form.create_role()
    return json.dumps(dict(
        data = role
    )), 201

@api.route('/<role_id>', methods=['PATCH'])
def update_role(role_id):
    role = db.session.query(AdminRole).filter(
        AdminRole.id == role_id
    ).first()
    if not role:
        raise NotFound('no role id is "%d"' % role)
    form = RoleForm.create_api_form(obj=role)
    role = form.update_role(role)
    return json.dumps(role)

