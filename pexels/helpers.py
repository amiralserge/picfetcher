from typing import Callable


from .base import BaseEndpoint


class ResourceRetriever:
    _endpoint:BaseEndpoint = None
    _default_max:int = 80
    _resource_key:str = None

    def __init__(self, endpoint: BaseEndpoint, resource_key):
        self._endpoint = endpoint
        self._resource_key = resource_key
        self._params = None
        
    def retrieve(self, params, processing_method:Callable=None):
        _max = params.pop('max', None)
        _max = self._default_max if _max is None else _max
        self._params = params
        
        count = 0
        res = self._fetch(params)
        while res:
            for res_data in res.get(self._resource_key, []):
                count += 1
                yield processing_method(res_data) if processing_method else self._extract_data(res_data)
                if count >= _max:
                    return
                
            next_page = res.get('next_page')
            if not next_page:
                break

            _next_params = dict([token.split('=') for token in next_page.split('?')[1].split('&')])
            res = self._fetch(_next_params)

    def _fetch(self, params):
        return self._endpoint.get(params=params)

    def _extract_data(self, data):
        return data
