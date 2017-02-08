# coding: utf-8
import datetime
from flask import request
from flask_wtf import FlaskForm as BaseForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Email, Regexp
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from werkzeug.security import generate_password_hash, check_password_hash

from jting.libs.errors import FormError
from models import db, AdminUser, AdminRole


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
        DataRequired(),
        Email()
    ])
    name = StringField(validators=[DataRequired()])
    phone = StringField(validators=[
        DataRequired(),
    ])
    password = PasswordField(validators=[DataRequired()])

    def validate_username(self, field):
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


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])

    def validate_password(self, field):
        username = self.username.data

        user = db.session.query(AdminUser.username, AdminUser.password).filter(AdminUser.username == username)

        if not user or check_password_hash(user.password, field.data):
            raise StopValidation('Invalid username or password')


class RoleForm(Form):
    name = StringField(validators=[
        DataRequired()
    ])
    remarks = StringField()
    permission = StringField()

    def validate_name(self, field):
        name = db.session.query(AdminRole).filter(AdminRole.name == field.data).first()
        if not name:
            raise StopValidation('name has been existed.')

    def validate_permission(self, field):
        pass