from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, Token, UserCreateOut
from dependencies import get_db
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/users')


@router.post('/register', tags=['Users'], response_model=UserCreateOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo usuário."""
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return db_user


@router.post('/login', response_model=Token, tags=['Users'])
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint para o login."""
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Usuário ou senha incorretos.')
    
    token = create_access_token({'sub': user.id})
    return {'access_token': token, 'token_type': 'bearer'}