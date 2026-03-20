import pytest
from fastapi.testclient import TestClient
from main import app
from app.tests.conftest import client


# fixture





# Testes


def test_get_home(client: TestClient):
    response = client.get('/words/list_words')
    assert response.status_code == 200