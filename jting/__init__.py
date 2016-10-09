# coding: utf-8

def register_base(app):
    from flask import request

    from jting.models import db

    db.init_app(app)

def register_app_blueprints(app):
    from jting.views import front

    app.register_blueprint(front.bp, url_prefix='')

def create_app(config=None):
    from .app import create_app
    app = create_app(config)
    register_base(app)
    register_app_blueprints(app)
    return app