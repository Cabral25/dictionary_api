import pytest
from fastapi.testclient import TestClient
from main import app


# fixture


@pytest.fixture(scope='function')
def client():
    client = TestClient(app)
    return client


# Testes


def test_get_home(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200