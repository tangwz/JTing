# coding: utf-8
import datetime
from flask import request
from flask_wtf import FlaskForm as BaseForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Optional
from wtforms.validators import Email, Regexp
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from werkzeug.security import generate_password_hash, check_password_hash

from settings import ALL_PERMS
from models import db, AdminUser, AdminRole
from jting.libs.errors import FormError, Denied


class Form(BaseForm):
    @classmethod
    def create_api_form(cls, obj=None):
        formdata = MultiDict(request.get_json())
        form = cls(formdata=formdata, obj=obj, csrf_enabled=False)
        form._obj = obj
        if not form.validate():
            raise FormError(form)
        return form

    def _validate_obj(self, key, value):
        obj = getattr(self, '_obj', None)
        return obj and getattr(obj, key) == value


class UserForm(Form):
    username = StringField(validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9]+$')
    ])
    email = StringField(validators=[
        Optional(),
        Email()
    ])
    name = StringField()
    phone = StringField()
    password = PasswordField()

    def validate_username(self, field):
        if self._validate_obj('username', field.data):
            return
        if db.session.query(AdminUser).filter(AdminUser.username == field.data.lower()).first():
            raise StopValidation('Username has been registered.')

    def create_user(self):
        user = AdminUser(
            username = self.username.data.lower(),
            email = self.email.data,
            name = self.name.data,
            phone = self.phone.data,
            addtime = datetime.datetime.now(),
            password = generate_password_hash(self.password.data),
        )
        with db.auto_commit():
            db.session.add(user)
        return user

    def update_user(self, user):
        keys = ['email', 'name', 'phone']

        for k in keys:
            value = self.data.get(k)
            if value:
                setattr(user, k, value)

        with db.auto_commit():
            db.session.add(user)
        return user


class RoleForm(Form):
    name = StringField(validators=[
        DataRequired()
    ])
    remarks = StringField()
    permission = StringField(validators=[
        DataRequired()
    ])

    def validate_name(self, field):
        if self._validate_obj('name', field.data):
            return

        name = db.session.query(AdminRole).filter(AdminRole.name == field.data).first()
        if not name:
            raise StopValidation('name has been existed.')

    def validate_permission(self, field):
        if self._validate_obj('permission', field.data):
            return

        # permission must be splited by ','
        data = field.data.split(',')
        perms = [x.id for _, x in ALL_PERMS.iteritems()]
        for p in data:
            if p not in perms:
                raise Denied

    def create_role(self):
        role = AdminRole(
            name = self.name.data,
            remarks = self.remarks.data,
            permission = self.permission.data,
        )

        with db.auto_commit():
            db.session.add(role)
        return role

    def update_role(self, role):
        keys = ['name', 'remarks', 'permission']

        for k in keys:
            value = self.data.get(k)
            if value:
                setattr(role, k, value)

        with db.auto_commit():
            db.session.add(role)
        return role
