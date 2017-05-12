# coding: utf-8

import pytest
from jting.api.users import api


@pytest.fixture
def app():
    return api


@pytest.fixture
def test_client(app):
    return app.test_client()

