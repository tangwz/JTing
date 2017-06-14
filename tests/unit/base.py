# -*- coding: utf-8 -*-
import pytest
from jting import create_app


@pytest.fixture
def app():
    return create_app({"SECRET_KEY": "xxx"})


@pytest.fixture
def test_client(app):
    return app.test_client()
