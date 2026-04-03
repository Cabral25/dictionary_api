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


@pytest.mark.override_rate_limiter
def test_words_list_rate_limiter_works(client):
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
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_word_invalid_data_missing_word(client, admin_token):
    data = {
        'meaning': 'meaning'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token)
    print('PRINT DO TESTE test_create_word_invalid_data_missing_word ⬇')
    print(response.json())
    assert response.status_code == 422


"""@pytest.mark.no_clean
def test_create_word_duplicate_word(client: TestClient, admin_token):
    word1 = {'word': 'word1', 'meaning': '...'}
    response1 = client.post('/words/create_word', json=word1, headers=admin_token)
    assert response1.status_code == 201

    word2 = {'word': 'word1', 'meaning': '...'}
    response2 = client.post('/words/create_word/', json=word2, headers=admin_token)
    assert response2.status_code == 405"""
    

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
    data = {
        'word': 'palavra',
        'meaning': 'qualquer coisa'
    }
    create_response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    update_data = {
        'word': 'palavra',
        'meaning': 'significado atualizado',
        'example': 'isso é uma palavra'
    }
    response = client.patch(f'/words/edit/{word_id}', json=update_data, headers=admin_token)
    print('PRINT DO TESTE TEST_EDIT_WORD_SUCCESS ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 200
    
    update_word = db_session.query(Word).filter(Word.word_id == word_id).first()
    assert update_word.meaning == 'significado atualizado'
    assert update_word.word == 'palavra'
    assert update_word.example == 'isso é uma palavra'


def test_edit_word_not_authorized(client, admin_token_not_admin, admin_token, db_session):
    data = {
        'word': 'palavra',
        'meaning': 'qualquer coisa'
    }
    create_response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    update_data = {
        'word': 'palavra',
        'meaning': 'significado atualizado',
        'example': 'isso é uma palavra'
    }
    response = client.patch(f'/words/edit/{word_id}', json=update_data, headers=admin_token_not_admin)
    word = db_session.query(Word).filter(Word.word_id == word_id).first()
    print('PRINT DO TESTE TEST_EDIT_WORD_SUCCESS ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authorized'}
    assert word.meaning != 'significado atualizado'
    assert word.meaning == 'qualquer coisa'
    assert word.example is None


def test_edit_word_invalid_type(client, admin_token, db_session):
    data = {
        'word': 'palavra',
        'meaning': 'qualquer coisa'
    }
    create_response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    update_data = {
        'word': 2000,
        'meaning': 'significado atualizado',
        'example': 'isso é uma palavra'
    }
    response = client.patch(f'/words/edit/{word_id}', json=update_data, headers=admin_token)
    word = db_session.query(Word).filter(Word.word_id == word_id).first()
    print('PRINT DO TESTE TEST_EDIT_WORD_INVALID_TYPE ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'
    assert word.word == 'palavra'
    assert word.meaning != 'significado atualizado'
    assert word.meaning == 'qualquer coisa'
    assert word.example is None


def test_edit_word_null_values(client, admin_token, db_session):
    data = {
        'word': 'palavra',
        'meaning': 'qualquer coisa'
    }
    create_response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    update_data = {
        'word': None,
        'meaning': None,
        'example': 'isso é uma palavra'
    }
    response = client.patch(f'/words/edit/{word_id}', json=update_data, headers=admin_token)
    word = db_session.query(Word).filter(Word.word_id == word_id).first()
    print('PRINT DO TESTE TEST_EDIT_WORD_NULL_VALUES ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'
    assert response.json()['detail'][1]['msg'] == 'Input should be a valid string'
    assert word.word == 'palavra'
    assert word.meaning != 'significado atualizado'
    assert word.meaning == 'qualquer coisa'
    assert word.example is None


def test_edit_word_missing_values(client, admin_token, db_session):
    data = {
        'word': 'palavra',
        'meaning': 'qualquer coisa'
    }
    create_response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    update_data = {}
    response = client.patch(f'/words/edit/{word_id}', json=update_data, headers=admin_token)
    word = db_session.query(Word).filter(Word.word_id == word_id).first()
    print('PRINT DO TESTE TEST_EDIT_WORD_MISSING_VALUES ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Field required'
    assert response.json()['detail'][1]['msg'] == 'Field required'
    assert word.word == 'palavra'
    assert word.meaning != 'significado atualizado'
    assert word.meaning == 'qualquer coisa'
    assert word.example is None


def test_edit_word_word_not_found(client, admin_token):
    update_data = {
        'word': 'palavra',
        'meaning': 'significado atualizado',
        'example': 'isso é uma palavra'
    }
    response = client.patch(f'/words/edit/1', json=update_data, headers=admin_token)
    print('PRINT DO TESTE TEST_EDIT_WORD_WORD_NOT_FOUND ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 404
    assert response.json() == {'detail': 'Word not found'}


def test_edit_word_timestamp_updates(client, admin_token, db_session):
    data = {
        'word': 'palavra',
        'meaning': 'qualquer coisa'
    }
    create_response = client.post('/words/create_word/', json=data, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]
    word = db_session.query(Word).filter(Word.word_id == word_id).first()
    initial_updated_at = word.updated_at
    import time
    time.sleep(0.10)

    update_data = {
        'word': 'nova palavra',
        'meaning': 'qualquer sentido',
        'example': 'isso é uma palavra'
    }
    
    response = client.patch(f'/words/edit/{word_id}', json=update_data, headers=admin_token)
    db_session.refresh(word)
    print('PRINT DO TESTE TEST_EDIT_WORD_TIMESTAMP_UPDATES ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 200
    assert word.updated_at > initial_updated_at


def test_edit_word_without_token(client, admin_token):
    word = {
        'word': 'teste',
        'meaning': 'um teste'
    }
    create_response = client.post('/words/create_word/', json=word, headers=admin_token)
    word_id = create_response.json()['word_id'][0]
    assert create_response.status_code == 201

    updated_word = {
        'meaning': 'um teste atualizado'
    }
    response = client.patch(f'/words/edit/{word_id}', json=updated_word)
    print('PRINT DO TESTE TEST_EDIT_WORD_WITHOUT_TOKEN ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


"""def test_edit_word_duplicate(client, admin_token, db_session, create_words):
    # criar duas palavras
    create_words(2)

    # tentar atualizar word2 para word1 (duplicada)
    update_data = {
        'word': 'word_2º',
        'meaning': '...'
    }
    response = client.patch(f'/words/edit/1', json=update_data, headers=admin_token)
    print('PRINT DO TESTE TEST_EDIT_WORD_DUPLICATE ⬇')
    print(response.status_code, response.json())
    # assert response.status_code == 500
    for i in range(1, 2):
        word_db = db_session.query(Word).filter(Word.word_id == i).first()
        print(word_db.word)
        assert word_db.word"""



# tESTES DA ENDPOINT DELETE_WORD


def test_delete_word_success(client, admin_token, db_session):
    word = {'word': 'palavra', 'meaning': '...'}
    create_response = client.post('/words/create_word', json=word, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]
    

    response = client.delete(f'/words/delete/{word_id}', headers=admin_token)
    word_db = db_session.query(Word).filter(Word.word_id == word_id).first()
    assert response.status_code == 204
    assert response.content == b''
    assert word_db is None


def test_delete_word_word_not_found(client, admin_token):
    response = client.delete('/words/delete/5', headers=admin_token)
    print('PRINT DO TESTE TEST_DELETE_WORD_WORD_NOT_FOUND ⬇')
    print(response.status_code, response.json())
    assert response.status_code == 404
    assert response.json() == {'detail': 'Word not found'}


def test_delete_word_user_not_authorized(client, admin_token, admin_token_not_admin, db_session):
    word = {'word': 'word', 'meaning': '...'}
    create_response = client.post('/words/create_word/', json=word, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    response = client.delete(f'/words/delete/{word_id}', headers=admin_token_not_admin)
    word_db = db_session.query(Word).filter(Word.word_id == word_id).first()
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authorized'}
    assert word_db.word


def test_delete_word_user_not_authenticated(client, admin_token):
    word = {'word': 'word', 'meaning': '...'}
    create_response = client.post('/words/create_word/', json=word, headers=admin_token)
    assert create_response.status_code == 201
    word_id = create_response.json()['word_id'][0]

    response = client.delete(f'/words/delete/{word_id}')
    assert response.json() == {'detail': 'Not authenticated'}
    assert response.status_code == 401