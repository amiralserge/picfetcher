import pytest

from unittest import mock

from . import base
from .base import BaseEndpoint
from .exceptions import InvalidParamsException


class TestEndpoint:

    @staticmethod
    def get_endpoint_stub(_api_path, _required_params=None):
        class Stub(BaseEndpoint):
            api_path = _api_path
            required_params = _required_params

        return Stub

    @staticmethod
    def get_endpoint_stub_instance(_api_path, _required_params=None):
        StubCLass = TestEndpoint.get_endpoint_stub(_api_path, _required_params)
        return StubCLass(None)

    def test_get_path_params_keys(self):
        url = "http://domain.com/{categ_id}/{product_id}"
        url2 = "http://domain.com/{id}"
        assert BaseEndpoint._get_path_params_keys(url) == ['categ_id', 'product_id']
        assert BaseEndpoint._get_path_params_keys(url2) == ['id']

    def test_remove_path_params(self):
        params = dict(id=1000, per_page=10)
        self.get_endpoint_stub(_api_path='photo/{id}')._remove_path_params(params)
        assert params == dict(per_page=10)

    def test_get_url(self):
        assert self.get_endpoint_stub('search')._get_url() == f"{BaseEndpoint.base_url}search"

    def test_get_url_with_path_params(self):
        assert self.get_endpoint_stub(
            _api_path='photo/{id}'
        )._get_url(**dict(id='1000')) == f"{BaseEndpoint.base_url}photo/1000"

    @mock.patch.object(base.requests.Session, 'request')
    def test_get(self, request_mock):
        endpoint = self.get_endpoint_stub_instance(_api_path='v1/photos/{id}')
        endpoint.get(params=dict(id=1204, dummy='value'))
        request_mock.assert_called_with(
            method='get',
            url='https://api.pexels.com/v1/photos/1204',
            headers={'Accept-Content': 'application/json', 'Authorization': None},
            params={'dummy': 'value'}
        )

    def test_required_params_validation(self):
        endpoint = self.get_endpoint_stub_instance(_api_path='search', _required_params=['query'])
        with pytest.raises(
                InvalidParamsException,
                match="Missing required parameter 'query' on endpoint /search"):
            endpoint.get()

    def test_path_params_validation(self):
        endpoint = self.get_endpoint_stub_instance(_api_path='v1/photo/{id}')
        with pytest.raises(
                InvalidParamsException,
                match="Param 'id' is unresolved in url https://api.pexels.com/v1/photo/{id}"):
            endpoint.get(params=dict(some="value"))
