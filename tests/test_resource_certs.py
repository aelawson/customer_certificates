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
            'active': 0,
            'body': 'my test body'
        }
        result = client.simulate_post(
            '/users/{user_id}/certificates'.format(user_id=user['id']),
            json=payload
        )
        data = result.json

        assert result.status == falcon.HTTP_201
        assert data['user_id'] == user['id']

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
