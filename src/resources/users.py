from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

import falcon
import json

from src.models.user import User

class UsersResource:
    """
    Resource for creating users
    """

    def on_post(self, req, resp):
        """
        Handles POST requests to the /users endpoint
        """
        try:
            payload = json.loads(req.stream.read().decode('utf-8'))

            user = User(
                name=payload['name'],
                email=payload['email'],
                password=payload['password']
            )

            self.session.add(user)
            self.session.commit()
        except KeyError:
            raise falcon.HTTPBadRequest(
                description='Missing one or more of the following fields: name, email, or password'
            )
        except IntegrityError:
            raise falcon.HTTPConflict(
                description='User with this email already exists'
            )

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({ 'id': user.id })

class UserResource:
    """
    Resource for retrieving or deleting a user
    """

    def on_get(self, req, resp, **kwargs):
        """
        Handles GET requests to the /users/{user_id} endpoint
        """
        try:
            user = self.session.query(User).filter(
                User.id == kwargs.get('user_id')
            ).one()
        except KeyError:
            raise falcon.HTTPBadRequest(
                description='Missing one or more of the following fields: name, email, or password'
            )
        except NoResultFound:
            raise falcon.HTTPNotFound(
                description='User does not exist'
            )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })

    def on_delete(self, req, resp):
        """
        Handles DELETE requests to the /users/{user_id} endpoint
        """
        pass
