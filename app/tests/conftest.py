import pytest
from fastapi.testclient import TestClient
from .config import engine_test, TestingSessionLocal
from ..main import app
from dependencies import get_db
from rate_limit import rate_limiter
import uuid
from models import Word, User
from sqlalchemy import event, text
from database import Base


@pytest.fixture(scope='session', autouse=True)
def create_table():
    """Cria as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine_test)
    print('As tabelas foram criadas')
    yield
    Base.metadata.drop_all(bind=engine_test)
    print('As tabelas foram destruídas')


@pytest.fixture
def db_session():
    connection = engine_test.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    # cria SAVEPOINT
    session.begin_nested()

    # garante que cada commit cria novo SAVEPOINT
    @event.listens_for(session, 'after_transaction_end')
    def restart_savepoint(sess, trans):
        if not trans.nested:
            sess.begin_nested()

    yield session

    print('Closing session')
    session.close()
    print('Destroying database data...')
    transaction.rollback()
    print('Closing connection...')
    connection.close()
    print('Done')


@pytest.fixture(autouse=True)
def clean_db(db_session):
    db_session.execute(text('TRUNCATE TABLE words, users RESTART IDENTITY CASCADE;'))
    db_session.commit()


@pytest.fixture
def client(db_session):

    def override_get_db():
        print('Override ativo', end=', ')
        print('Banco do db_session: ', db_session.bind.engine.url)
        yield db_session

    def override_rate_limiter():
        return None

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[rate_limiter] = override_rate_limiter

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture # <-- needs refactoring
def admin_token(client: TestClient):
    unique = str(uuid.uuid4())

    username = f'admin_{unique}'
    email = f'{unique}@test.com'
    password = f'password_{unique}'
    # cria usuário admin
    client.post(
        '/users/register', json={
            'username': username,
            'email': email,
            'password': password,
            'is_admin': True
        }
    )

    # login
    response = client.post('/users/login', data={'username': username, 'password': password, 'grant_type': 'password'})
    # print(response.status_code)
    # print(response.json())
    token = response.json()['access_token']

    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def create_words(client: TestClient, admin_token):
    def create(n: int):
        
        for i in range(1, n + 1):
            res = client.post(
                '/words/create_word/',
                json={
                    'word': f'word_{i}º.',
                    'meaning': 'test'
                },
                headers=admin_token
            )
            print('PRINT DA FIXTURE CREATE_WORDS ⬇')
            print(f'word: {i}, status code: {res.status_code}, json: {res.json()}')
            assert res.status_code in (200, 201), res.json()
        print('url do banco:', engine_test.url)
    return create
