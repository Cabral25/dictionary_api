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

        🔷 JWT
        🔷 JWS
        🔷 criptografia
"""

"""
    O que é JWT?

        JWT siginifica JSON Web Token
        É basicamente um token (string) que carrega informações
        do usuário de forma segura. Exemplo:

            eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

        Ele é composto de 3 partes:

            HEADER.PAYLOAD.SIGNATURE

        🔷 Payload (a parte importante). Exemplo:

            {
                'sub': '1', --> id do usuário
                'exp': 17100000 --> data de expiração do token
            }

        🔷 Signature: é o que garante que ninguém pode
          alterar o token

    jwt é um módulo dentro do jose que tem funções como:

        🔷 jwt.encode()
        🔷 jwt.decode()

    Funciona como um crachá:

        🔷 sub ➡ quem é você
        🔷 exp ➡ validade do crachá
        🔷 SECRET_KEY ➡ selo oficial que impede falsificação
        🔷 ALGORITHM ➡ tipo do selo
"""

load_dotenv()

# Chave secreta usada para assinar o token (deve ser longa e aleatória);
# protege o token
SECRET_KEY = os.getenv('SECRET_KEY')
# Algoritmo usado para assinar o token (usa a SECRET_KEY e uma função de hash segura),
# definido para HS256 (HMAC + SHA256); define como proteger o token
ALGORITHM = os.getenv('ALGORITHM')
# Define a data/hora que o token expira (definido pra 30 minutos),
# depois desse tempo, o token se torna inválido; define até quando vale o token
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
        
        "Esses dados pertencem a esse usuário, foram assinados com
        minha chave secreta e só são válidos até tal momento."
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=float(ACCESS_TOKENS_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
