
from .base import BaseEndpoint


class PhotoSearchEndpoint(BaseEndpoint):
    api_path = 'search'
    required_params = ['query']

class PhotoEndpoint(BaseEndpoint):
    api_path = 'photos/{id}'

