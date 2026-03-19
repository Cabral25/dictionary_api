import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL  = 'postresql://postgres:Postc@pital25/test_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()