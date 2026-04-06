from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Postc%40pital25@localhost:5432/dictionary_api_tests'

engine_test = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)