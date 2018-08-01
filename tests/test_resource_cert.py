import base64
import falcon
import pytest
import json
import random

class TestCertResource():

    def test_cert_activate_success(self, client, cert):
        result = client.simulate_patch(
            '/users/{user_id}/certificates/{certificate_id}/active'.format(
                user_id=cert['user_id'],
                certificate_id=cert['id']
            ),
            json={ 'active': True }
        )

        assert result.status == falcon.HTTP_202

        data = result.json

        assert data['id'] == cert['id']
        assert data['active'] == 1

    def test_cert_activate_success_notify(self, client, cert):
        result = client.simulate_patch(
            '/users/{user_id}/certificates/{certificate_id}/active'.format(
                user_id=cert['user_id'],
                certificate_id=cert['id']
            ),
            json={ 'active': True, 'notify': True }
        )

        assert result.status == falcon.HTTP_202

        data = result.json

        assert data['id'] == cert['id']
        assert data['active'] == 1

    def test_cert_activate_fail_missing_field(self, client, cert):
        result = client.simulate_patch(
            '/users/{user_id}/certificates/{certificate_id}/active'.format(
                user_id=cert['user_id'],
                certificate_id=cert['id']
            ),
            json={ }
        )

        assert result.status == falcon.HTTP_400

    def test_cert_activate_fail_user_not_found(self, client, cert):
        result = client.simulate_patch(
            '/users/{user_id}/certificates/{certificate_id}/active'.format(
                user_id=-1,
                certificate_id=cert['id']
            ),
            json={ 'active': True }
        )

        assert result.status == falcon.HTTP_404

    def test_cert_activate_fail_cert_not_found(self, client, cert):
        result = client.simulate_patch(
            '/users/{user_id}/certificates/{certificate_id}/active'.format(
                user_id=cert['user_id'],
                certificate_id=-1
            ),
            json={ 'active': True }
        )

        assert result.status == falcon.HTTP_404

    def test_cert_deactivate_fail_already_in_state(self, client, cert):
        result = client.simulate_patch(
            '/users/{user_id}/certificates/{certificate_id}/active'.format(
                user_id=cert['user_id'],
                certificate_id=cert['id']
            ),
            json={ 'active': False }
        )

        assert result.status == falcon.HTTP_400
