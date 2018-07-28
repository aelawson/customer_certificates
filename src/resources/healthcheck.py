import falcon
import json

class Healthcheck:
    """
    Resource used as an application healthcheck"
    """

    def on_get(self, req, resp):
        """
        Handles GET requests to the healthcheck
        """
        # API is healthy
        services_checks = {
            'api': 1
        }

        # Check DB healthiness
        try:
            self.session.execute('SELECT 1')
            services_checks['database'] = 1
        except Exception:
            services_checks['database'] = 0

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(services_checks)
