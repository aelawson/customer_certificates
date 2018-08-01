import base64
import falcon
import pytest
import json
import random

class TestCertsResource():

    def test_cert_create(self, client, user, private_key):
        b64_encoded_key = base64.b64encode(private_key).decode('utf-8')

        payload = {
            'private_key': b64_encoded_key,
            'active': False,
            'body': 'my test body'
        }
        result = client.simulate_post(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            json=payload
        )
        data = result.json

        assert result.status == falcon.HTTP_201
        assert data['user_id'] == user['id']

    def test_cert_create_fail_user_not_found(self, client, private_key):
        b64_encoded_key = base64.b64encode(private_key).decode('utf-8')

        payload = {
            'private_key': b64_encoded_key,
            'active': False,
            'body': 'my test body'
        }
        result = client.simulate_post(
            '/users/{user_id}/certificates'.format(user_id=-1),
            json=payload
        )

        assert result.status == falcon.HTTP_404

    def test_cert_list(self, client, user, generate_n_certs):
        result = client.simulate_get('/users/{user_id}/certificates'.format(user_id=user['id']))
        certs = result.json

        assert result.status == falcon.HTTP_200
        assert len(certs) == 0

        generated_certs = generate_n_certs(5, user)

        assert len(generated_certs) == 5

        result = client.simulate_get('/users/{user_id}/certificates'.format(user_id=user['id']))
        certs = result.json

        assert result.status == falcon.HTTP_200
        assert len(certs) == 5

    def test_cert_list_active(self, client, user, generate_n_certs):
        result = client.simulate_get('/users/{user_id}/certificates'.format(user_id=user['id']))
        certs = result.json

        assert result.status == falcon.HTTP_200
        assert len(certs) == 0

        generated_certs = generate_n_certs(5, user)
        generated_active_certs = generate_n_certs(3, user, active=True)

        assert len(generated_certs) == 5
        assert len(generated_active_certs) == 3

        result = client.simulate_get(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            params={ 'active': 'true' }
        )
        certs = result.json

        assert result.status == falcon.HTTP_200
        assert len(certs) == 3

    def test_cert_list_active_false(self, client, user, generate_n_certs):
        result = client.simulate_get('/users/{user_id}/certificates'.format(user_id=user['id']))
        certs = result.json

        assert result.status == falcon.HTTP_200
        assert len(certs) == 0

        generated_certs = generate_n_certs(5, user)
        generated_active_certs = generate_n_certs(3, user, active=True)

        assert len(generated_certs) == 5
        assert len(generated_active_certs) == 3

        result = client.simulate_get(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            params={ 'active': 'false' }
        )
        certs = result.json

        assert result.status == falcon.HTTP_200
        assert len(certs) == 8

    def test_cert_list_active_fail_bad_query(self, client, user, generate_n_certs):
        result = client.simulate_get(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            params={ 'active': 1 }
        )

        assert result.status == falcon.HTTP_422

        result = client.simulate_get(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            params={ 'active': 'abc' }
        )

        assert result.status == falcon.HTTP_422

    def test_cert_create_fail_malformed(self, client, user):
        payload = 'adsfasdf'
        result = client.simulate_post(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            json=payload
        )

        assert result.status == falcon.HTTP_400
