import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import declarative_base
from app.tests.config import engine, Base, TestingSessionLocal
from ..main import app
from app.dependencies import get_db


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