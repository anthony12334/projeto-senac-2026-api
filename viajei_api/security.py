from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

SECRET_KEY = 'your-very-secret-and-exclusive-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
contexto_senha = PasswordHash.recommended()


def create_token_access(dados: dict):
    para_codificar = dados.copy()
    # BR = UCT-03
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    para_codificar.update({'exp': expire})
    jwt_codificar = encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_codificar


def get_password_hash(password: str):
    return contexto_senha.hash(password)


def verify_paasword(plain_password: str, hashed_password: str):
    return contexto_senha.verify(plain_password, hashed_password)
