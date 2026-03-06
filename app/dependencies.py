from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_db():
    """
        Gerencia o ciclo de vida da sessão do banco. Quando a requisição 
        termina (com sucesso ou erro), o finally executa db.close().
    """
    db = SessionLocal() # Cria a sessão
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(User).filter(User.id == payload['sub']).first() # <-- first? first what?
    if not user:
        raise HTTPException(status_code=401)
    return user


def admin_required(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403)
    return user