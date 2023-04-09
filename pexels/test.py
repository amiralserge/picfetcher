from unittest import mock
from unittest.mock import Mock

from . import api
from .api import Endpoint

class TestEndpoint:

    @staticmethod
    def get_endpoint_stub(_api_path):
        class Stub(Endpoint):
            api_path = _api_path

        return Stub

    @staticmethod
    def get_endpoint_stub_instance(_api_path):
        StubCLass = TestEndpoint.get_endpoint_stub(_api_path)
        return StubCLass(None)

    def test_get_path_params_keys(self):
        url = "http://domain.com/{categ_id}/{product_id}"
        assert Endpoint._get_path_params_keys(url) == ['categ_id', 'product_id']

    def test_remove_path_params(self):
        params = dict(id=1000, per_page=10)
        self.get_endpoint_stub(_api_path='photo/{id}')._remove_path_params(params) 
        assert params == dict(per_page=10)

    def test_get_url(self):
        assert self.get_endpoint_stub('search')._get_url() == f"{Endpoint.base_url}search"

    def test_get_url_with_path_params(self):
        assert self.get_endpoint_stub(
            _api_path='photo/{id}'
        )._get_url(**dict(id='1000')) == f"{Endpoint.base_url}photo/1000"

    @mock.patch.object(api.requests.Session, 'request')
    def test_get(self, request_mock):
        endpoint = self.get_endpoint_stub_instance(_api_path='photos/{id}')
        endpoint.get(params=dict(id=1204, dummy='value'))
        request_mock.assert_called_with(
            method='get', 
            url='https://api.pexels.com/v1/photos/1204', 
            headers={'Accept-Content': 'application/json', 'Authorization': None}, 
            params={'dummy': 'value'}
        )
