import requests
import re

from typing import (Any, Dict, List)


class Endpoint:
    base_url = "https://api.pexels.com/v1/"
    api_path = None
    _url_path_param_regex = re.compile(r"\{(\w+)\}")
    _default_headers = {
        'Accept-Content': 'application/json'
    }


    def __init__(self, apli_key):
        self.session = requests.session()
        self.api_key = apli_key

    def get(self, **kwargs) -> Any:
        kwargs.pop('url', None)
        url_params = kwargs.pop('params', {})
        path_params = self._remove_path_params(url_params)
        url = self._get_url(**path_params)
        return self.request('get', url=url, params=url_params, **kwargs)

    @classmethod
    def _remove_path_params(cls, params: Dict) -> Dict:
        return {key: params.pop(key) for key in cls._get_path_params_keys(cls.api_path) if key in params}
    
    @classmethod
    def _get_url(cls, **path_params) -> str:
        url = f'{cls.base_url}{cls.api_path}'
        params_kw = {k: path_params.get(k) for k in cls._get_path_params_keys(url) if k in path_params}
        return url.format(**params_kw) if params_kw else url

    @classmethod
    def _get_path_params_keys(cls, url) -> List[str]:
        return cls._url_path_param_regex.findall(url)

    def request(self, method, url, **kwargs) -> Any:
        headers = dict(self._default_headers)
        headers.update(kwargs.pop('headers', None) or {})
        headers.update(self._get_authentication_header())
        response = self.session.request(method=method, url=url, headers=headers, **kwargs)
        return self._process_response(response)

    def _get_authentication_header(self):
        return {'Authorization': self.api_key}

    def _process_response(self, response):
        response.raise_for_status()
        return response.json()
