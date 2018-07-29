import falcon
import pytest
import json

class TestHealthcheck():
    def test_users_create_success(self, client, fake):
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

    def test_users_create_fail_conflict(self, client, fake):
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

        result = client.simulate_post(
            '/users',
            json=payload
        )

        assert result.status == falcon.HTTP_409

    def test_users_create_fail_invalid(self, client, fake):
        payload = {
            'name': fake.name(),
            'email': fake.email()
        }
        result = client.simulate_post(
            '/users',
            json=payload
        )

        assert result.status == falcon.HTTP_400

        payload = {
            'email': fake.email(),
            'password': 'password'
        }
        result = client.simulate_post(
            '/users',
            json=payload
        )

        assert result.status == falcon.HTTP_400

        payload = {
            'name': fake.name(),
            'password': 'password'
        }
        result = client.simulate_post(
            '/users',
            json=payload
        )

        assert result.status == falcon.HTTP_400
