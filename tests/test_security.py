from jwt import decode

from viajei_api.security import SECRET_KEY, create_token_access


def test_jwt():

    data = {'test': 'test'}
    token = create_token_access(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
