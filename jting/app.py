# coding: utf-8

import os
from datetime import datetime
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict
        if isinstance(o, datetime):
            return o.strftime('%Y-&m-%dT%H:%M:%SZ')
        return JSONEncoder.default(self, o)

class Flask(_Flask):
    json_encoder = JSONEncoder
    jinja_options = dict(
        trim_blocks = True,
        lstrip_blocks = True,
        extensions = [
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
        ]
    )

def create_app(config = None):
    pass