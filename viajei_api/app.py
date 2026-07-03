from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from viajei_api.database import get_session
from viajei_api.models import User
from viajei_api.schemas.message import Message
from viajei_api.schemas.user import UserList, UserPublic, UserSchema
from viajei_api.security import (
    create_token_access,
    get_password_hash,
    verify_paasword,
)

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Bem vindo!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = session.scalar(select(User).where((User.email == user.email)))

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email já existe'
        )
    hashed_password = get_password_hash(user.password)

    db_user = User(email=user.email, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, Session: Session = Depends(get_session)
):
    users = Session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}
    return {'users': database}


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not founf'
        )

    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'user deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def ver_user_test(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
              detail='Usuário não existe'
        )
    return database[user_id - 1]


@app.post('/auth')
def retrive_token(
    dados_form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):

    user = session.scalar(select(user). where(User.email == dados_form.username))

    if not user:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            detail='esse email não existe'
        )

    if not verify_paasword(dados_form.password, user.password):
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            detail='Email ou senha incorretos'
        )
    Token_access = create_token_access(dados={'sub': user.email})
    return {'access_token': create_token_access, 'token_type': 'bearer'}
