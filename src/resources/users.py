from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import NoResultFound

import falcon
import json

from src.models.user import User
from src.services.caching_query import FromCache
from src.services.hash import HashService

class UsersResource:
    """
    Resource for creating users
    Endpoint: /users
    """

    def on_post(self, req, resp):
        """
        Handles POST requests.
        Creates a user resource.
        """
        try:
            payload = json.loads(req.stream.read().decode('utf-8'))
            hashed_pass = HashService.hash(payload['password'])

            user = User(
                name=payload['name'],
                email=payload['email'],
                password=hashed_pass
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
        except DataError:
            raise falcon.HTTPUnprocessableEntity(
                description='Bad request format'
            )

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({ 'id': user.id })

class UserResource:
    """
    Resource for retrieving or deleting a user
    Endpoint: /users/{user_id}
    """

    def on_get(self, req, resp, **kwargs):
        """
        Handles GET requests.
        Retrieves a user resource.
        """
        try:
            user = self.session.query(User)\
                .options(FromCache('default'))\
                .filter(
                    User.id == kwargs.get('user_id')
                )\
                .one()
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

    def on_delete(self, req, resp, **kwargs):
        """
        Handles DELETE requests.
        Deletes a user resource.
        """
        try:
            user_query = self.session.query(User)\
                .options(FromCache('default'))\
                .filter(
                    User.id == kwargs.get('user_id')
                )\

            # Invalidate the cache
            user = user_query.one()
            user_query.invalidate()

            self.session.delete(user)
        except NoResultFound:
            raise falcon.HTTPNotFound(
                description='User does not exist'
            )

        resp.status = falcon.HTTP_204
