from fastapi.testclient import TestClient
from app.tests.conftest import client
from conftest import db_session
from models import Word
from sqlalchemy.orm import Session



# Testes


# Testes da endpoint list_words


def test_get_words_list(client: TestClient):
    response = client.get('/words/list_words')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_pagination_page_1(client: TestClient, db_session: Session):
    for i in range(10):
        db_session.add(Word())