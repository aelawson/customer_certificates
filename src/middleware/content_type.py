import falcon

class ContentTypeMiddleware:
    """
    Middleware for restricting / enforcing request and response formats.
    """

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                description='JSON is the only supported response format'
            )

        if req.method in ('POST', 'PUT'):
            if req.content_type and 'applicaton/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    description='JSON is the only supported request format'
                )
