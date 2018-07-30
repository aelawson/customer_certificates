import base64
import falcon
import json

from sqlalchemy.orm.exc import NoResultFound

from src.models.certificate import Certificate

class CertificatesResource:
    """
    Resource for creating and retrieving certificates
    """

    def on_post(self, req, resp, **kwargs):
        """
        Handles POST requests to the /users/{user_id}/certificates endpoint
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

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({ 'id': cert.id, 'user_id': cert.user_id })

    def on_get(self, req, resp, **kwargs):
        """
        Handles GET requests to the /users/{user_id}/certificates endpoint
        Lists certificate resources for a user.
        """
        try:
            certs = self.session.query(Certificate)\
                .filter(Certificate.user_id == kwargs.get('user_id')).all()
        except NoResultFound:
            raise falcon.HTTPNotFound(
                description='No certificates found for the specified user'
            )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(list(
            map(lambda c: { 'id': c.id, 'user_id': c.user_id, 'body': c.body }, certs)
        ))
