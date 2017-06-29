# coding: utf-8
from .base import ApiBlueprint
from flask import jsonify
from jting.forms import HubForm
from jting.models import db, PyHub
from jting.libs.utils import jwt_auth
from jting.libs.page import pagination_query
from jting.libs.ratelimit import ratelimit
from jting.libs.errors import NotConfidence, NotFound

api = ApiBlueprint('hubs')


@api.route('/', methods=['GET'])
@ratelimit(limit=300, per=60)
def list_hubs():
    hubs, pagination = pagination_query(PyHub, PyHub.id, status=1)
    return jsonify(hubs), 200


@api.route('/', methods=['POST'])
def create_hub():
    payload = jwt_auth()
    form = HubForm.create_api_form()
    hub = form.create_hub(payload)
    return jsonify(hub), 201


@api.route('/<hid>', methods=['PUT'])
def update_hub(hid):
    payload = jwt_auth()
    form = HubForm.create_api_form()
    hub = form.update_hub(hid, payload)
    return jsonify(hub), 200


@api.route('/<hid>', methods=['DELETE'])
def delete_hub(hid):
    payload = jwt_auth()
    if not payload['admin']:
        raise NotConfidence()
    hub = db.session.query(PyHub).filter_by(id=hid).first()
    if not hub:
        raise NotFound()
    hub.status = -1
    with db.auto_commit():
        db.session.add(hub)
    return jsonify(hub), 200

