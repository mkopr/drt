import logging

import requests
from app.settings import API_KEY, COLLECTOR_REQ_URL

logger = logging.getLogger(__name__)


class RequestHandler:
    BASE_URL = COLLECTOR_REQ_URL

    def __init__(self):
        self.session = requests.Session()

    def request(self, method='GET', **kwargs):
        url = self._prepare_url(**kwargs)
        method_handler = getattr(self.session, method.lower())
        response = self._request(method_handler, url)
        return self.check_status_code(response)

    @classmethod
    def _request(cls, handler, url):
        url = cls.BASE_URL + url
        return handler(url)

    def prepare_response(self, response):
        try:
            logger.error(f'[INFO][request_handler.py][prepare_response] {response.json}')
            return response.json()
        except Exception:
            logger.error(f'[ERROR][request_handler.py][prepare_response] {response.text}')
            return response.text

    def check_status_code(self, response):
        if not response.status_code != 200:
            return self.prepare_response(response)
        return None

    def _prepare_url(self, **kwargs):
        url = f'?apikey={API_KEY}&t={kwargs["title"]}'
        return url
