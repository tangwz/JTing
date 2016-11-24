# coding: utf-8

def register_base(app):
    from flask import request

    from jting.models import db

    db.init_app(app)

def register_app_blueprints(app):
    from jting.views import front, account

    app.register_blueprint(front.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')

def register_not_found(app):
    from flask import request
    from jting.libs.errors import NotFound

    @app.errorhandler(404)
    def handle_not_found(e):
        if request.path.startswith('/api/'):
            return NotFound('URL')
        return e

def create_app(config=None):
    from .app import create_app
    app = create_app(config)
    register_base(app)
    register_app_blueprints(app)
    return app