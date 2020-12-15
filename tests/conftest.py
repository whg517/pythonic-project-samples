"""Test config"""

import pytest
from fastapi.testclient import TestClient

from example_blog import server


@pytest.fixture
def test_client():
    """Fast api test client factory"""
    client = TestClient(app=server.app)
    yield client
