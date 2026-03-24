import pytest
from fastapi.testclient import TestClient
from app.tests.config import engine, Base, TestingSessionLocal
from ..main import app
from app.dependencies import get_db
import uuid
# from database import Base


@pytest.fixture(scope='session', autouse=True)
def create_table():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    return client


@pytest.fixture
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
    print(response.status_code)
    print(response.json())
    token = response.json()['access_token']

    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def create_words(client: TestClient, admin_token):
    def create(n):
        for i in range(n):
            client.post(
                '/words/create_word/',
                json={
                    'word': f'word{i}',
                    'meaning': 'test'
                },
                headers=admin_token
            )
    return create