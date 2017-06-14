# -*- coding: utf-8 -*-

from jsonschema import validate, SchemaError, ValidationError


PYUSER_SCHEMA = {
    'type': 'object',
    'required': ['account', 'password', 'nickname'],
    'properties': {
        'account': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string', 'minLength': 6},
        'avatar': {'type': 'string', 'format': 'uri'},
        'nickname': {'type': 'string'},
        'about': {'type': 'string'}
    }
}


def safe_validate(data, schema):
    try:
        validate(data, schema)
        return True
    except SchemaError as e:
        print e
    except ValidationError as e:
        print e
    except Exception as e:
        print e
    return False

