import requests

from src.services.config import Config

class CertificateService:
    """
    Service encapsulating functionality for notifying the external certificate service.
    """
    NOTIFY_PATH = '/post'

    @classmethod
    def notify(cls, certificate_id, active):
        """
        Notify service of change to certificate active status.
        """
        url = 'http://{host}{path}'.format(
            host=Config['cert-service']['host'],
            path=cls.NOTIFY_PATH
        )
        resp = requests.post(
            url,
            json={ 'id': certificate_id, 'active': active }
        )
        resp.raise_for_status()
