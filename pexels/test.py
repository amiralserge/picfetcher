from .api import Endpoint

class TestEndpoint:

    def test_get_url(self):
        endpoint = Endpoint(None)
        endpoint.api_path = 'search'
        assert endpoint._get_url() == f"{Endpoint.base_url}search"

    def test_get_url_with_path_params(self):
        endpoint = Endpoint(None)
        endpoint.api_path = 'photo/{id}'
        assert endpoint._get_url(id=1000) == f"{Endpoint.base_url}photo/1000"
