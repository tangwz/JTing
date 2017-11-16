# coding: utf-8
from datetime import datetime
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return _JSONEncoder.default(self, o)


class Flask(_Flask):
    json_encoder = JSONEncoder
    jinja_options = dict(
        # strip whitespace in jinja2
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=[
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
        ]
    )


# Factory method
def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    return app
