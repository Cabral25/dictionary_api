from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKENS_EXPIRE_MINUTES = os.getenv('ACCESS_TOKENS_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=['bcrypt'])


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str | bytes, hashed: str | bytes | None):
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKENS_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)