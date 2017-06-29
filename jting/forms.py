# -*- coding: utf-8 -*-
from flask import request
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Optional
from wtforms.validators import Email, Length, Regexp, URL
from wtforms.validators import StopValidation
from werkzeug.datastructures import MultiDict
from werkzeug.security import generate_password_hash, check_password_hash
from jting.models import db, PyUser, PyHub
from jting.config import DEFAULT_AVATAR
from jting.libs.errors import FormError, NotConfidence, NotFound


class Form(FlaskForm):
    @classmethod
    def create_api_form(cls, obj=None):
        formdata = MultiDict(request.get_json())
        form = cls(formdata=formdata, obj=obj)
        if not form.validate_on_submit():
            raise FormError(form)
        return form


class UserForm(Form):
    nickname = StringField(validators=[
        DataRequired(),
        Length(min=3, max=20),
    ])


class EmailForm(Form):
    account = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])


class RegisterForm(UserForm, EmailForm):
    def validate_nickname(self, field):
        entry = db.session.query(PyUser.id).filter_by(nickname=field.data).first()
        if entry:
            raise StopValidation('Nickname has been registered!')

    def validate_email(self, field):
        entry = db.session.query(PyUser.id).filter_by(account=field.data).first()
        if entry:
            raise StopValidation('Email has been registered!')

    def create_user(self):
        user = PyUser(
            nickname=self.nickname.data,
            account=self.account.data,
            password=generate_password_hash(self.password.data),
            avatar=DEFAULT_AVATAR
        )
        with db.auto_commit():
            db.session.add(user)
            db.session.flush()
        return user


class LoginForm(EmailForm):
    def validate_password(self, field):
        account = self.account.data
        password = field.data
        user = db.session.query(PyUser).filter_by(account=account).first()
        if not user or not check_password_hash(user.password, password):
            raise StopValidation('Invalid password!')
        self.user = user


class HubForm(Form):
    title = StringField(validators=[
        DataRequired(),
        Length(min=3)
    ])
    link = StringField(validators=[DataRequired(), URL()])
    desc = StringField(validators=[Optional()])
    tag = StringField(validators=[Optional()])

    def validate_title(self, field):
        entry = db.session.query(PyHub.title).filter_by(title=field.data).first()
        if entry:
            raise StopValidation('Title has been existed!')

    def validate_link(self, field):
        entry = db.session.query(PyHub.link).filter_by(title=field.data).first()
        if entry:
            raise StopValidation('Link has been existed!')

    def create_hub(self, payload):
        # verify jwt
        if not payload.get('admin', False):
            raise NotConfidence()

        uid = payload['sub']
        nickname = db.session.query(PyUser.nickname).filter_by(id=uid).first()[0]

        hub = PyHub(
            title=self.title.data,
            link=self.link.data,
            desc=self.desc.data,
            tag=self.tag.data,
            user_id=uid,
            nickname=nickname,
            status=1,
        )
        with db.auto_commit():
            db.session.add(hub)
        return hub

    def update_hub(self, hid, payload):
        hub = db.session.query(PyHub).filter_by(id=hid, status=1).first()

        if not hub:
            raise NotFound()

        if not payload.get('admin', False) and payload['sub'] != hub.id:
            raise NotConfidence()

        hub.title = self.title.data
        hub.link = self.link.data
        hub.desc = self.desc.data
        hub.modify_id = payload['sub']
        with db.auto_commit():
            db.session.add(hub)
        return hub

