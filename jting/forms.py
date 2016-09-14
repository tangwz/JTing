# coding: utf-8

import hashlib

from flask import request
from flask_wtf import Form as BaseForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields import TextAreaField, IntegerField
from wtforms.validators import DataRequired, optional
from wtforms.validators import Email, Length, Regexp, URL
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from libs.errors import FormError
from libs.cache import cache

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
        Length(min=3, max=30),
        Regexp(r'^[a-z0-9]+$'),
    ])
    password = PasswordField(validators=[DataRequired()])

class PasswordForm(Form):
    password = PasswordField(validators=[DataRequired()])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Email()])

    def validata_email(self, field):
        pass

class UserProfileForm(Form):
    name = StringField(validators=[Length(min=0, max=24)])
    description = StringField(validators=[Length(min=0, max=280)])