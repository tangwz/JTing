# coding: utf-8

import hashlib

from flask import request
from flask_wtf import Form as BaseForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields import TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms.validators import Email, Length, Regexp, URL
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from jting.libs.errors import FormError
from jting.models import db, User

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
        Length(min=3, max=20),
        Regexp(r'^[a-z0-9]+$'),
    ])
    password = PasswordField(validators=[DataRequired()])

class PasswordForm(Form):
    password = PasswordField(validators=[DataRequired()])

class LoginForm(PasswordForm):
    username = StringField('Username or Email', validators=[DataRequired()])

    def validate_password(self, field):
        username = self.username.data
        if '@' in username:
            user = User.cache.filter_first(email=username)
        else:
            user = User.cache.filter_first(username=username)

        if not user or not user.check_password(field.data):
            raise StopValidation('Invalid account or password')

        self.user = user

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Email()])

    def validate_email(self, field):
        if User.cache.filter_first(email=field.data):
            raise StopValidation('Email has been registered.')

class RegisterForm(UserForm, EmailForm):
    def validate_username(self, field):
        if User.cache.filter_first(username=field.data):
            raise StopValidation('Username has been registered.')

    def create_user(self):
        user = User(
            username = self.username.data,
            email = self.email.data,
        )
        user.password = self.password.data
        user.role = User.ROLE_ACTIVE
        with db.auto_commit():
            db.session.add(user)
        return user