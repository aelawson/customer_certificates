import falcon
import pytest
import json

class TestUserResource():
    def test_user_get_success(self, client, fake):
        name = fake.name()
        email = fake.email()

        payload = {
            'name': name,
            'email': email,
            'password': 'password'
        }
        result = client.simulate_post(
            '/users',
            json=payload
        )
        post_data = result.json

        assert result.status == falcon.HTTP_201


        result = client.simulate_get('/users/{user_id}'.format(user_id=post_data['id']))
        get_data = result.json

        assert result.status == falcon.HTTP_200

        assert get_data.get('id') == post_data['id']
        assert get_data.get('name') == name
        assert get_data.get('email') == email

    def test_user_get_fail_not_found(self, client, fake):
        result = client.simulate_get('/users/-1')

        assert result.status == falcon.HTTP_404

    def test_user_delete_success(self, client, user):
        result = client.simulate_delete('/users/{user_id}'.format(user_id=user['id']))

        assert result.status == falcon.HTTP_204

    def test_user_delete_cert_cascade_success(self, client, user, generate_n_certs):
        generated_certs = generate_n_certs(10, user)

        assert len(generated_certs) == 10

        result = client.simulate_delete('/users/{user_id}'.format(user_id=user['id']))

        assert result.status == falcon.HTTP_204

        result = client.simulate_get('/users/{user_id}/certificates'.format(user_id=user['id']))

        assert result.status == falcon.HTTP_200

        data = result.json
        assert len(data) == 0

    def test_user_delete_fail(self, client, user):
        result = client.simulate_delete('/users/{user_id}'.format(user_id=-1))

        assert result.status == falcon.HTTP_404
