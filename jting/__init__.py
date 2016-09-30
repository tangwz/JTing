# coding: utf-8

def register_base(app):
    from flask import request

    from jting.models import db

    db.init_app(app)

def create_app(config=None):
    from .app import create_app
    app = create_app(config)
    register_base(app)
    return app