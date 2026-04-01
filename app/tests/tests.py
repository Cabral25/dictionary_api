from fastapi.testclient import TestClient
from .conftest import client, admin_token, admin_token_not_admin, db_session, client_no_savepoint
from models import Word
import pytest



# Testes da endpoint list_words


def test_get_words_list(client: TestClient, create_words):
    create_words(5)
    response = client.get('/words/list_words')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_pagination_page_1(client: TestClient, create_words):
    create_words(10)
    response = client.get('/words/list_words/?page=1')
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_pagination_page_2(client: TestClient, create_words):
    create_words(10)
    response = client.get('/words/list_words/?page=2')
    print(response.json())
    print(f'status code: {response.status_code}')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_pagination_last_page(client, create_words):
    create_words(8)
    response = client.get('/words/list_words/?page=2')
    print('PRINT DO TESTE ⬇')
    print(response.status_code, response.json(), f'total de resultados: {len(response.json())}')
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_invalid_page(client):
    response = client.get('/words/list_words/?page=0')
    assert response.status_code == 422


def test_words_list_rate_limiter_works(client):
    """"
        Para o correto funcionamente deste teste, desabilite
        o override de rate_limiter na fixture client.
    """
    for i in range(5):
        response = client.get('/words/list_words/')
        assert response.status_code == 200

    response = client.get('/words/list_words/')
    assert response.status_code == 429



# Testes da endpoint create_word


def test_create_word_success(client: TestClient, admin_token):
    data = {
        'word': 'word1',
        'meaning': 'any meaning'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token)
    print('PRINT DO TESTE TEST_GET_CREATE_WORD ⬇')
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {'msg': 'created', 'word_id': [1]}


def test_create_word_user_not_authorized(client, admin_token_not_admin):
    data = {
        'word': 'word2',
        'meaning': 'meaning'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token_not_admin)
    print('PRINT DO TESTE TEST_CREATE_WORD_USER_NOT_AUTHORIZED ⬇')
    print(response.json())
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authorized'}


def test_create_word_without_token(client):
    data = {
        'word': 'word2',
        'meaning': 'meaning'
    }
    response = client.post('/words/create_word/', json=data)
    assert response.status_code == 401


def test_create_word_invalid_data_missing_word(client, admin_token):
    data = {
        'meaning': 'meaning'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token)
    print('PRINT DO TESTE test_create_word_invalid_data_missing_word ⬇')
    print(response.json())
    assert response.status_code == 422


@pytest.mark.no_clean
def test_create_word_duplicate_word(client_no_savepoint: TestClient, admin_token):
    data = {
        'word': 'duplicate',
        'meaning': 'meaning'
    }
    response1 = client_no_savepoint.post('/words/create_word/', json=data, headers=admin_token)
    assert response1.status_code == 201

    # Tentar duplicar
    response2 = client_no_savepoint.post('/words/create_word/', json=data, headers=admin_token)
    assert response2.status_code == 500

    
def test_create_word_with_example(client, admin_token):
    data = {
        'word': 'word_with_example',
        'meaning': 'meaning',
        'example': 'example text'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert response.status_code == 201
    assert 'word_id' in response.json()


def test_create_word_persisted_in_db(client, db_session, admin_token):
    data = {
        'word': 'word',
        'meaning': 'meaning'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert response.status_code == 201

    word = db_session.query(Word).filter(Word.word == 'word').first()
    assert word is not None
    assert word.meaning == 'meaning'
    assert word.created_by is not None



# Testes da endpoint edit_word


def test_edit_word_success(client: TestClient, admin_token, db_session):
    word = db_session.add(Word(
        word='palavra',
        meaning='...'
    ))
    data = {
        'meaning': 'qualquer coisa'
    }
    response = client.patch(f'/words/edit/{word.word_id}', headers=admin_token, json=data)
    assert response.status_code == 200