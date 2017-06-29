# coding: utf-8

from flask import json
from werkzeug.exceptions import HTTPException
from werkzeug._compat import text_type


class APIException(HTTPException):
    code = 400
    error = 'Invalid request'

    def __init__(self, code=None, error=None, description=None, response=None):
        if code is not None:
            self.code = code
        if error is not None:
            self.error = error
        super(APIException, self).__init__(description, response)

    def get_body(self, environ=None):
        return text_type(json.dumps(dict(
            error=self.error,
            description = self.description
        )))

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class SchemaError(APIException):
    error = 'Invalid format'


class FormError(APIException):
    error = 'Invalid format'

    def __init__(self, form, response=None):
        self.form = form
        super(FormError, self).__init__(None, response)

    def get_body(self, environ=None):
        return text_type(json.dumps(dict(
            error=self.error,
            description=self.form.errors
        )))


class NotAuth(APIException):
    code = 401
    error = 'Require login'


class NotConfidence(APIException):
    code = 403
    error = 'require confidence'
    description = 'Only confidential clients are allowed'


class NotFound(APIException):
    code = 404
    error = 'Not found'


class Denied(APIException):
    code = 403
    error = 'Permission denied'


class LimitExceeded(APIException):
    code = 429
    error = 'Too many requests'


class ServerError(APIException):
    code = 500
    error = 'Internal Server Error'
