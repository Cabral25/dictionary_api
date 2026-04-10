from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import SECRET_KEY, ALGORITHM

# o OAuth2PasswordBearer é um helper do fastapi que faz duas coisas:
# ° Lê e retorna o token do header de requisição
# ° Integra com o Swagger (botão Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def get_db():
    """
        Gerencia o ciclo de vida da sessão do banco. Quando a requisição 
        termina (com sucesso ou erro), o finally executa db.close().

        Uma sessão é o objeto que gerencia a comunicação entre o código
        python e o banco de dados. Ela funciona como uma ponte:

            🔷 Mantém um cache local do objetos manipulados
            🔷 Controla transações
            🔷 Decide quando enviar comandos SQL de fato para o banco
            🔷 Permite trabalhar com objetos python sem precisar escrever
                SQL manualmente.
    """
    db = SessionLocal() # Cria a sessão
    try:
        yield db
    finally:
        db.close() # fecha a sessão


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # first retorna o primeiro resultado encontrado dessa consulta.
    # Esse método aplica um limite de 1 ao SQL gerado
    # Equivale a: SELECT * FROM users WHERE user_id = payload['sub'] LIMIT 1;
    user = db.query(User).filter(User.user_id == payload['sub']).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user


def admin_required(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Not authorized')
    return user
