# -*- coding: utf-8 -*-
import json
from .base import app, test_client


def test_register(app, test_client):
    resp = test_client.post('/api/v1/session/new', data='{}', content_type='application/json')
    assert resp.status_code == 400

    resp = test_client.post(
        '/api/v1/session/new',
        data=json.dumps(dict(account='test@jting.com', password='test-password', nickname='test')),
        content_type='application/json')
    if resp.status_code == 201:
        data = json.loads(resp.data)
        assert data['account'] == 'test@jting.com'
    elif resp.status_code == 400:
        assert json.loads(resp.data)['error'] == 'register failed.'
    print resp.headers


def test_login(app, test_client):
    resp = test_client.post('/api/v1/session/login', data='{}', content_type='application/json')
    assert resp.status_code == 400
    assert json.loads(resp.data)['description'] == 'No user.'

    resp = test_client.post(
        '/api/v1/session/login',
        data=json.dumps(dict(account='test@jting.com', password='test-password')),
        content_type='application/json')
    assert resp.status_code == 200
    assert json.loads(resp.data)['nickname'] == 'test'


def test_logout(app, test_client):
    resp = test_client.delete('/api/v1/session/')
    assert resp.status_code == 403
    rv = json.loads(resp.data)
    assert rv['error'] == 'require confidence'
