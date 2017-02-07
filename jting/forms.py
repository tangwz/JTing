# coding: utf-8

from flask import request
from flask_wtf import FlaskForm as BaseForm
from wtforms import SelectMultipleField
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Email, Regexp
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from werkzeug.security import generate_password_hash, check_password_hash

from jting.libs.errors import FormError
from models import db, AdminUser


class Form(BaseForm):
    @classmethod
    def api_form(cls, obj=None):
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
        Regexp(r'^[0-9]+$')
    ])
    password = PasswordField(validators=[DataRequired()])
    role = SelectMultipleField(validators=[DataRequired()])


class Password(Form):
    password = PasswordField(validators=[DataRequired()])


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])

    def validate_password(self, field):
        username = self.username.data

        user = db.session.query(AdminUser.username, AdminUser.password).filter(AdminUser.username == username)

        if not user or check_password_hash(user.password, field.data):
            raise StopValidation('Invalid username or password')


class RegisterForm(UserForm):
    def validate_username(self, field):
        if db.session.query(AdminUser).filter(AdminUser.username == field.data.lower()).first():
            raise StopValidation('Username has been registered.')

    def create_user(self):
        user = AdminUser(
            username = self.username.data.lower(),
            email = self.email.data,
            name = self.name.data,
            phone = self.phone.data,
            password = generate_password_hash(self.password.data),
            role = self.role.data,
        )
        with db.auto_commit():
            db.session.add(user)
        return user