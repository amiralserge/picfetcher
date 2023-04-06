import requests


class Endpoint:
    base_url = "https://api.pexels.com/v1/"
    api_path = None
    path_params_keys = []
    _default_headers = {
        'Accept-Content': 'application/json'
    }

    def __init__(self, apli_key):
        self.session = requests.session()
        self.api_key = apli_key

    def request(self, method, url, **kwargs):
        headers = kwargs.pop('headers', None) or {}
        headers.update(self._get_authentication_header())
        response = self.session.request(method=method, url=url, headers=headers, **kwargs)
        return self._process_response(response)

    def _get_authentication_header(self):
        return {'Authorization', self.api_key}

    def _process_response(self, response):
        response.raise_for_status()
        return response.json()

    def get(self, **params):
        params = dict(params)
        url = self._get_url(params)
        return self.request('get', url=url, params=params)

    def _get_url(self, **params):
        url = f'{self.base_url}{self.api_path}'
        params_kw = {}
        for k in list(params.keys()):
            if "{key}".format(key=k) in url:
                params_kw[k] = params.pop(k)
        return url.format(**params_kw) if params_kw else url
