# coding: utf-8

from jsonlint_flask import create_app

app = create_app()

app.run('0.0.0.0', port=5005, debug=True)