import abc
from typing import Any, Callable, Generator

from .base import BaseEndpoint, ListResourceEndpoint


class AbstractResourceRetriever(abc.ABC):
    _endpoint:BaseEndpoint = None

    def __init__(self, endpoint:BaseEndpoint) -> None:
        self._endpoint = endpoint

    @abc.abstractmethod
    def retrieve(self, params, processing_method:Callable=None) -> Any:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _extract_data(self, data) -> Any:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _fetch(self, params) -> Any:
        raise NotImplementedError()


class SingleResourceRetriever(AbstractResourceRetriever):
    
    def retrieve(self, params, processing_method: Callable = None) -> Any:
        res = self._fetch(params=params)
        return processing_method(res) if processing_method else self._extract_data(res)
    
    def _fetch(self, params) -> Any:
        return self._endpoint.get(params=params)
    
    def _extract_data(self, data) -> Any:
        return data


class ListResourceRetriever(AbstractResourceRetriever):
    _endpoint:ListResourceEndpoint = None
    _default_max:int = 80
    _resource_key:str = None

    def __init__(self, endpoint: ListResourceEndpoint):
        super().__init__(endpoint)
        
    def retrieve(self, params, processing_method:Callable=None) -> Generator:
        _max = params.pop('max', None)
        _max = self._default_max if _max is None else _max
        count = 0
        res = self._fetch(params)
        while res:
            for res_data in res.get(self._endpoint.resource_key, []):
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
