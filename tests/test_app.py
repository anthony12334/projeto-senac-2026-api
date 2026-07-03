from http import HTTPStatus

from fastapi.testclient import TestClient

from viajei_api.schemas.user import UserPublic


def test_create_user(client):

    response = client.post(
        '/users',
        json={
            'email': 'joao@test.com',
            'password': 'senha123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'joao@test.com',
        'id': 1,
    }


def test_read_users(client: TestClient):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


# def test_ver_user_200(client):
#     response = client.get('/users/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'email': 'joao@test.test',
#         'id': 1,
#     }


def test_delete_user(client):

    response = client.delete('/users/1')

    response.status_code == HTTPStatus.OK
    response.json() == {'menssage': 'user deleted'}


def test_get_token(client, user):
    response = client.post('/auth',
        data={"username": user.email, "password": user.clean_passwd}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


# def test_ver_user_erro404(client):
#     response = client.get('/users/666')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Usuário não existe'}


# def delete_user_404(client):
#     response = client.delete('/users/666')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Usuário não encontrado'}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}
