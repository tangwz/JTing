# -*- coding: utf-8 -*-
from flask import request, jsonify
from .base import ApiBlueprint
from jsonlint_flask.lints import UserJson
from jsonlint_flask.libs.errors import APIException


api = ApiBlueprint('index')
@api.route('/', methods=['POST'])
def index():
    user = UserJson(request.get_json())
    if not user.validate():
        raise APIException()

    return jsonify(
        nickname=user.nickname.data,
        account=user.account.data,
        cars=user.cars.data
    ), 200
