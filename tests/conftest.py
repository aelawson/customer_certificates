import base64
import falcon
import pytest
import random

from faker import Faker
from falcon import testing

import app

"""
Helper functions
"""

def create_private_key():
    return bytearray(random.getrandbits(8) for _ in range(100))

def create_cert(client, user, private_key):
    b64_encoded_key = base64.b64encode(private_key).decode('utf-8')

    payload = {
        'user_id': user['id'],
        'private_key': b64_encoded_key,
        'active': False,
        'body': 'my test body'
    }
    result = client.simulate_post(
        '/users/{user_id}/certificates'.format(user_id=user['id']),
        json=payload
    )

    assert result.status == falcon.HTTP_201

    return result.json

def create_user(client, fake):
    payload = {
        'name': fake.name(),
        'email': fake.email(),
        'password': 'password'
    }
    result = client.simulate_post(
        '/users',
        json=payload
    )

    assert result.status == falcon.HTTP_201

    return result.json

"""
Fixtures
"""

@pytest.fixture(scope='session')
def client(request):
    return testing.TestClient(app.create())

@pytest.fixture(scope='session')
def fake(request):
    return Faker()

@pytest.fixture(scope='function')
def user(request, client, fake):
    return create_user(client, fake)

@pytest.fixture(scope='function')
def cert(request, client, user, private_key):
    return create_cert(client, user, private_key)

@pytest.fixture(scope='function')
def generate_n_certs(request, client):
    def __inner(n, user):
        return [
            create_cert(client, user, create_private_key()) for _ in range(n)
        ]

    return __inner

@pytest.fixture(scope='function')
def private_key(request):
    return create_private_key()

@pytest.fixture(scope='function')
def private_key_n_bytes(request):
    def __inner(n):
        return bytearray(random.getrandbits(8) for _ in range(n))

    return __inner
