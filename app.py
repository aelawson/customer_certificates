import falcon

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
    app = falcon.API()
    app.add_route('/hello', HelloResource())

    return app

app = create()