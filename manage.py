# coding: utf-8

from jting import create_app

app = create_app()

app.run('0.0.0.0', port=5005)