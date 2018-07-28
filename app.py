import falcon

from src.middleware.session import RequestSessionMiddleware
from src.services.db import DbSession

class HelloResource:
    """
    Resource used as a test resource that says "Hello World!"
    """

    def on_get(self, req, resp):
        """
        Handles GET requests to Hello Resource
        """
        resp.status = falcon.HTTP_200
        resp.body = 'Hello World!'

def create():
    """
    Creates app instance and instantiates middleware / routes.
    """
    app = falcon.API(middleware=[
        RequestSessionMiddleware(DbSession)
    ])

    app.add_route('/hello', HelloResource())

    return app

app = create()