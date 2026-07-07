from http import HTTPStatus

from viajei_api.schemas.user import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):

    # Act / When
    response = client.get('/')

    # Assert / Then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Bem vindo!'}


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.json() == {'users': [user_schema]}


def test_delete_user(client, user):

    # When
    response = client.delete('/users/1')

    # Then
    response.status_code == HTTPStatus.OK
    response.json() == {'message': 'User deleted'}


def test_get_token(client, user):

    # GIVEN
    response = client.post(
        '/auth', data={'username': user.email, 'password': user.clean_passwd}
    )

    # WHEN
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'token_type' in token
    assert 'access_token' in token

def test_create_story(autheticated_user):

    response = client.post(
        "/story",
        json={
    "author": "joao",
    "title":"se essa casa fosse minha",
    "story": "era uma vez"
   } )
    
    breakpoint

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() =={
    "id": "1",
    "email": "example@example.com",
    "title": "se essa casa fosse minha",

    }