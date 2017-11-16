# -*- coding: utf-8 -*-
from jsonlint import Json
from jsonlint.fields import StringField, ListField
from jsonlint.validators import DataRequired, Email, Length
from jsonlint_flask.libs.errors import APIException


class UserJson(Json):
    nickname = StringField(validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    account = StringField(validators=[Email(), DataRequired()])
    cars = ListField(StringField())

    def validate_cars(self, field):
        if 'BMW' in field.data:
            # I don't like BMW.
            raise APIException(error='Invalid format')
