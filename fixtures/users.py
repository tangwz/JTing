# coding: utf-8

from jting.models import User

def iter_admin_users():
    yield {
        "username": "root",
        "email": "jting@example.com",
        "reputation": 1000,
        "role": 9
    }

    yield {
        "username": "tangwz",
        "email": "tangwz@example.com",
        "reputation": 1000,
        "role": 8
    }

def iter_data():
    for data in iter_admin_users():
        user = User(**data)
        user.password = 'jting'
        yield user