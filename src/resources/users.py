from sqlalchemy.exc import IntegrityError

import falcon
import json

from src.models.user import User

class Users:
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
        print("success")
        resp.body = json.dumps({ 'id': user.id })
