from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL  = 'postgresql://postgres:Postc%40pital25@localhost:5432/dictionary_api_tests'

engine_test = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base = declarative_base()