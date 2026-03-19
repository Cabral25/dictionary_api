import pytest
from fastapi.testclient import TestClient
from main import app
from fixtures import client


# fixture


@pytest.fixture(scope='function')
def client():
    client = TestClient(app)
    return client


# Testes


def test_get_home(client: TestClient):
    response = client.get('/words/list_words')
    assert response.status_code == 200