from fastapi.testclient import TestClient
from app.tests.conftest import client
from app.tests.conftest import db_session, create_words
from models import Word
from sqlalchemy.orm import Session



# Testes


# Testes da endpoint list_words


def test_get_words_list(client: TestClient):
    response = client.get('/words/list_words')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_pagination_page_1(client: TestClient, create_words):
    create_words(10)
    response = client.get('/words/list_words/?page=1')
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_pagination_page_2(client: TestClient, create_words):
    create_words(10)
    response = client.get('/words/list_words/?page=2')
    print(response.json())
    print(f'status code: {response.status_code}')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_pagination_last_page(client: TestClient, create_words):
    create_words(7)
    response = client.get('/words/list_words/?page=2')
    print(response.status_code, response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2