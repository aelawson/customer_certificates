class RequestSessionMiddleware:
    """
    Middleware for opening and closing a new SQLAlchemy session for each request.

    Docs: http://falcon.readthedocs.io/en/stable/api/middleware.html
    """

    def __init__(self, session):
        self.session = session

    def process_resource(self, req, resp, resource, params):
        """
        Instantiate the session on the resource the request was routed to.
        """
        resource.session = self.session()

    def process_response(self, req, resp, resource, req_succeeded):
        """
        Remove the ression after the request has been handled.
        Rollback if the request failed.
        """
        if hasattr(resource, 'session'):
            if not req_succeeded:
                resource.session.rollback()

        self.session.remove()
