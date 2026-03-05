from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, Token
from ..database import get_db
from ..auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return {'msg': 'user created'}


@router.post('/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401)
    
    token = create_access_token({'sub': user.id})
    return {'access_token': token, 'token_type': 'bearer'}