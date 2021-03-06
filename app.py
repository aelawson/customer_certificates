import falcon

from src.middleware.error_serializer import ErrorSerializer
from src.middleware.content_type import ContentTypeMiddleware
from src.middleware.session import RequestSessionMiddleware

from src.resources.healthcheck import Healthcheck
from src.resources.users import UserResource, UsersResource
from src.resources.certificate import CertificatesResource, CertificateActiveResource

from src.services.db import DB

def create():
    """
    Creates app instance and instantiates middleware / routes.
    """
    app = falcon.API(middleware=[
        ContentTypeMiddleware(),
        RequestSessionMiddleware(DB.get_db_session())
    ])
    app.set_error_serializer(ErrorSerializer)

    app.add_route('/healthcheck', Healthcheck())
    app.add_route('/users', UsersResource())
    app.add_route('/users/{user_id:int}', UserResource())
    app.add_route('/users/{user_id:int}/certificates', CertificatesResource())
    app.add_route('/users/{user_id:int}/certificates/{certificate_id:int}/active', CertificateActiveResource())

    return app

app = create()