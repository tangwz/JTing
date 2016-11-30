# coding: utf-8

from sqlalchemy.exc import IntegrityError
from jting.models import db

def commit(module):
    for m in module.iter_data():
        db.session.add(m)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def run():
    from fixtures import users
    commit(users)
