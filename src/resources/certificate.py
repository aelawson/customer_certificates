import base64
import falcon
import json

from requests.exceptions import HTTPError
from sqlalchemy import exists
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from src.models.certificate import Certificate
from src.models.user import User
from src.services.caching_query import FromCache
from src.services.certificate import CertificateService

class CertificatesResource:
    """
    Resource for creating and retrieving certificates
    Endpoint: /users/{user_id}/certificates
    """

    def on_post(self, req, resp, **kwargs):
        """
        Handles POST requests.
        Creates a certificate resource for a user.
        """
        try:
            payload = json.loads(req.stream.read().decode('utf-8'))
            private_key = base64.b64decode(payload['private_key'])

            cert = Certificate(
                user_id=kwargs.get('user_id'),
                private_key=private_key,
                active=payload['active'],
                body=payload['body']
            )

            self.session.add(cert)
            self.session.commit()
        except KeyError:
            raise falcon.HTTPBadRequest(
                description='Missing one or more of the following fields: private_key, active, or body'
            )
        except IntegrityError:
            raise falcon.HTTPNotFound(
                description='User does not exist'
            )
        except DataError:
            raise falcon.HTTPUnprocessableEntity(
                description='Bad request format - make sure all fields are the proper data type.'
            )

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({ 'id': cert.id, 'user_id': cert.user_id })

    def on_get(self, req, resp, **kwargs):
        """
        Handles GET requests.
        Lists certificate resources for a user.
        """
        user_exists = self.session.query(
            exists().where(User.id == kwargs.get('user_id'))
        ).scalar()

        if not user_exists:
            raise falcon.HTTPNotFound(
                description='User does not exist'
            )

        cert_query = self.session.query(Certificate)\
            .filter(Certificate.user_id == kwargs.get('user_id'))

        filter_active = req.get_param('active', default='false')

        if filter_active not in ['true', 'false']:
            raise falcon.HTTPUnprocessableEntity(
                description='Bad request format - active query parameter must be "true" or "false".'
            )
        elif filter_active == 'true':
            cert_query = cert_query.filter(Certificate.active == True)

        certs = cert_query.all()

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(list(
            map(
                lambda c: { 'id': c.id, 'body': c.body, 'active': c.active },
                certs
            )
        ))

class CertificateActiveResource():
    """
    Resource for activating/deactivating a certificate for a user.
    Endpoint: /users/{user_id}/certificates/{certificate_id}/active
    """

    def on_patch(self, req, resp, **kwargs):
        """
        Handles PATCH requests.
        Updates active state for a certificate resource.
        """
        payload = json.loads(req.stream.read().decode('utf-8'))

        if len(payload) != 1 or 'active' not in payload:
            raise falcon.HTTPBadRequest(
                description='Must provide only the following fields: active'
            )

        # Update active status in the DB
        try:
            cert_query = self.session.query(Certificate)\
                .options(FromCache('default'))\
                .filter(Certificate.id == kwargs.get('certificate_id'))\
                .filter(Certificate.user_id == kwargs.get('user_id'))\

            # Invalidate the cache
            cert = cert_query.one()
            cert_query.invalidate()

            if payload['active'] == cert.active:
                raise falcon.HTTPBadRequest(
                    description='Certificate is already in the requested active state'
                )

            cert.active = payload['active']
        except NoResultFound:
            raise falcon.HTTPNotFound(
                description='No certificate found for the specified user and certificate'
            )

        # Notify external service of change
        try:
            CertificateService.notify(cert.id, cert.active)
        except HTTPError as e:
            raise falcon.HTTPServiceUnavailable(
                description="Internal service error: {error}".format(error=e)
            )

        resp.status = falcon.HTTP_202
        resp.body = json.dumps({
            'id': cert.id,
            'active': cert.active
        })
