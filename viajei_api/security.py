from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from viajei_api.database import get_session
from viajei_api.models import User

CHAVE_SECRETA = 'your-very-secret-and-exclusive-key'
ALGORITMO = 'HS256'
TOKEN_ACESSO_MINUTOS_EXPIRAR = 30

contexto_senha = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth')


def create_token(dados: dict):
    para_codificar = dados.copy()
    # BR = UTC-03
    expira = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=TOKEN_ACESSO_MINUTOS_EXPIRAR
    )

    para_codificar.update({'exp': expira})
    jwt_codificado = encode(para_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)

    return jwt_codificado


def get_password_hash(password: str):
    return contexto_senha.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return contexto_senha.verify(plain_password, hashed_password)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    try:
        payload = decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        email: str = payload.get('sub')

        if email is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='User not authenticated',
                headers={'WWW-Authenticate': 'Bearer'},
            )

    except AttributeError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user = session.scalar(select(User).where(User.email == email))

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User credentials are invalid',
        )

    return user
