import falcon

from src.middleware.error_serializer import ErrorSerializer
from src.middleware.content_type import ContentTypeMiddleware
from src.middleware.session import RequestSessionMiddleware

from src.resources.healthcheck import Healthcheck

from src.services.db import DBService

def create():
    """
    Creates app instance and instantiates middleware / routes.
    """
    app = falcon.API(middleware=[
        ContentTypeMiddleware(),
        RequestSessionMiddleware(DBService.get_db_session())
    ])
    app.set_error_serializer(ErrorSerializer)

    app.add_route('/healthcheck', Healthcheck())

    return app

app = create()