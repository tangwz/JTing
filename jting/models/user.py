# coding: utf-8

import datetime

from werkzeug.utils import cached_property
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from sqlalchemy import Column
from sqlalchemy import String, Unicode, DateTime
from sqlalchemy import SmallInteger, Integer
from sqlalchemy.orm.attributes import get_history
from .base import db, Base

class User(Base):
    __tablename__ = 'jting_user'

    ROLE_SUPER = 9
    ROLE_ADMIN = 8
    ROLE_STAFF = 7
    ROLE_VERIFIED = 4
    ROLE_SPAMMER = -9
    ROLE_ACTIVE = 1

    id = Column(Integer, primary_key=True)
    username = Column(String(24), unique=True)
    email = Column(String(255), unique=True)
    _password = Column('password', String(100))

    name = Column(Unicode(40))
    description = Column(Unicode(280))

    role = Column(SmallInteger, default=0)
    reputation = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User:%s>' % self.username

    def __str__(self):
        return self.name or self.username

    def keys(self):
        return (
            'id', 'username', 'name', 'description',
            'role', 'reputation', 'is_active',
            'created_at', 'updated_at',
        )

    @cached_property
    def is_active(self):
        return self.role > 0

    @cached_property
    def label(self):
        if self.role >= self.ROLE_STAFF:
            return 'staff'
        if self.role == self.ROLE_VERIFIED:
            return 'verified'
        if self.role == self.ROLE_SPAMMER:
            return 'spammer'
        return None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)