from fastapi.testclient import TestClient
from .conftest import client, admin_token



# Testes


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


def test_words_list_rate_limiter_works():
    pass



# Testes da endpoint create_word


def test_get_create_word(client: TestClient, admin_token):
    data = {
        'word': 'word1',
        'meaning': 'any meaning'
    }
    response = client.post('/words/create_word/', json=data, headers=admin_token)
    print('PRINT DO TESTE TEST_GET_CREATE_WORD ⬇')
    print(response.json())
    assert response.status_code == 200