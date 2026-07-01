from http import HTTPStatus

from fastapi.testclient import TestClient


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
    # Arrange / Given

    # Act / When
    response = client.get('/')

    # Assert / Then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Bem vindo!'}


def test_create_user(client: TestClient):

    response = client.post(
        '/users/',
        json={
            'email': 'joao@test.test',
            'password': 'senha123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'joao@test.test',
        'id': 1,
    }


def test_read_users(client: TestClient):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'joao@test.test',
                'id': 1,
            }
        ]
    }


def test_ver_user_200(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'joao@test.test',
        'id': 1,
    }


def test_delete_user(client):

    response = client.delete('/users/1')

    response.status_code == HTTPStatus.OK
    response.json() == {'menssage': 'user deleted'}


def test_ver_user_erro404(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não existe'}


def delete_user_404(client):
    response = client.delete('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
