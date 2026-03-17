from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from jose import jwt
from dotenv import load_dotenv
import os

"""
    pwdlib é uma biblioteca que implementa algoritmos
    seguros de hashing de senha. Cuida de coisas como:

        🔷 salt automático (valor aleatório adicionado à senha antes do hash)
        🔷 algoritmos seguros
        🔷 verificação de senha
        🔷 parâmetros de segurança

    Algoritmos comuns (o mais recomendado é o argon2):

        🔷 bcrypt
        🔷 argon2
        🔷 scrypt
        🔷 pbkdf2
"""


"""
    python-jose é o módulo usado para criar, validar e
    decodificar tokens. Ele implementa padrões como:

        ° JWT
        ° JWS
        ° criptografia
"""

"""
    O que é JWT?

        JWT siginifica JSON Web Token
        É basicamente um token (string) que carrega informações
        do usuário de forma segura. Exemplo:

            eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

        Ele é composto de 3 partes:

            HEADER.PAYLOAD.SIGNATURE

        ° Payload (a parte importante). Exemplo:

            {
                'sub': '1', --> id do usuário
                'exp': 17100000 --> data de expiração
            }

        ° Signature: é o que garante que ninguém pode
          alterar o token

    jwt é um módulo dentro do jose que tem funções como:

        ° jwt.encode()
        ° jwt.decode()
"""

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKENS_EXPIRE_MINUTES = os.getenv('ACCESS_TOKENS_EXPIRE_MINUTES')

password_hash = PasswordHash.recommended()
# Usa a configuração de hashing considerada segura atualmente.
# No caso do pwdlib, ele normalmente usa argon2id, que é um
# algoritmo moderno de hashing de senha


"""
    O que é um hash?

        Um hash é uma função que transforma um dado em outra
        sequência de caracteres de tamanho fixo. Exemplo:

            Senha --> minhasenha123
            Depois do hash --> $argon2id$v=19$m=65536,t=3,p=4$...

    Características importantes

        🔷Todo hash é unidirecional, você consegue fazer senha -> hash,
           mas não consegue fazer hash -> senha.

        🔷 Sempre gera a mesma saída:

            hash('senha123') -> abcdef
            hash('senha123') -> abcdef

        🔷 Pequenas mudanças mudam tudo:

            hash('senha123') -> abcdef
            hash('senha124') -> 91kfj2

    Usa-se hash para senha porque guardar senha em
    texto puro é extremamente perigoso. O que fica
    armazenado no banco de dados é o hash da senha,
    não a senha.

    Como o login funciona

        user digita a senha
        ⬇
        hash da senha digitada
        ⬇
        comparar com hash armazenado
        ⬇
        se igual ➡ login válido
"""

def hash_password(password: str):
    """
        Retorna o hash de password. O hash é a senha transformada
        em uma sequência de caracteres aleatórios
        determinados por um algoritmo (geralmente argon2).
    """
    return password_hash.hash(password)


def verify_password(password: str | bytes, hashed: str | bytes | None):
    """
        Compara a senha digitada com o hash dessa mesma
        senha guardada no banco de dados.
    """
    return password_hash.verify(password, hashed)


def create_access_token(data: dict):
    """
        Cria e retorna um token usado para identificar o usuário
        sem precisar de sessão no servidor. Exemplo:

            eyJhbGciOiJIUzI.eyJ0ZXN0ZSI6dzczNjg4OTEyfQ.kpHk_IfZGQEMoui4WO8cj
                 ⬇                   ⬇                          ⬇
               HEADER             PAYLOAD                   SIGNATURE
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=float(ACCESS_TOKENS_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


teste = hash_password('senha123')
print(teste)
# $argon2id$v=19$m=65536,t=3,p=4$wbE2P3FcFqnQwybsiwE75A$Jtnfp2vitZDnSaFESJQUcGgsJIyoLH1ddlf4xTU6zXg

testejwt = create_access_token({'teste': True})
print(f'token gerado: {testejwt}')
# token gerado: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXN0ZSI6dHJ1ZSwiZXhwIjoxNzczNjg4OTEyfQ.kpHk_IfZGQEMoui4WO8cjqbAPdfd0QtSdVVY-5v6DZ8