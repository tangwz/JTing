# -*- coding: utf-8 -*-
import time
from jting.libs.ratelimit import ratelimit


def test_ratelimit(app, test_client):
    @app.route('/', methods=['GET'])
    @ratelimit(limit=10, per=10)
    def index():
        return "test, ratelimit", 200

    resp = test_client.get('/')
    assert resp.status_code == 200
    for i in range(10):
        resp = test_client.get('/')
    assert resp.status_code == 429
    time.sleep(10)
    resp = test_client.get('/')
    assert resp.status_code == 200
